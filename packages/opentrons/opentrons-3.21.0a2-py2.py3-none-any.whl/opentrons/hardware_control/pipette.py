""" Classes and functions for pipette state tracking
"""
from dataclasses import asdict, replace
import logging
from typing import Any, Dict, Optional, Tuple, Union, TYPE_CHECKING

from opentrons.types import Point
from opentrons.config import pipette_config
from opentrons.config.feature_flags import enable_calibration_overhaul
from .types import CriticalPoint
from opentrons_shared_data.pipette import name_for_model

if TYPE_CHECKING:
    from opentrons_shared_data.pipette.dev_types import (
        PipetteModel, UlPerMmAction
    )

mod_log = logging.getLogger(__name__)


class Pipette:
    """ A class to gather and track pipette state and configs.

    This class should not touch hardware or call back out to the hardware
    control API. Its only purpose is to gather state.
    """

    DictType = Dict[str, Union[str, float, bool]]
    #: The type of this data class as a dict

    def __init__(self,
                 model: 'PipetteModel',
                 inst_offset_config: Dict[str, Tuple[float, float, float]],
                 pipette_id: str = None) -> None:
        self._config = pipette_config.load(model, pipette_id)
        self._name = name_for_model(model)
        self._model = model
        self._model_offset = self._config.model_offset
        self._current_volume = 0.0
        self._working_volume = self._config.max_volume
        self._current_tip_length = 0.0
        self._current_tiprack_diameter = 0.0
        self._fallback_tip_length = self._config.tip_length
        self._tip_overlap_map = self._config.tip_overlap
        self._has_tip = False
        self._pipette_id = pipette_id
        pip_type = 'multi' if self._config.channels == 8 else 'single'
        self._instrument_offset = Point(*inst_offset_config[pip_type])
        self._log = mod_log.getChild(self._pipette_id
                                     if self._pipette_id else '<unknown>')
        self._log.info("loaded: {}, instr offset {}"
                       .format(model, self._instrument_offset))
        self.ready_to_aspirate = False
        #: True if ready to aspirate
        self._aspirate_flow_rate\
            = self._config.default_aspirate_flow_rates['2.0']
        self._dispense_flow_rate\
            = self._config.default_dispense_flow_rates['2.0']
        self._blow_out_flow_rate\
            = self._config.default_blow_out_flow_rates['2.0']

    def update_instrument_offset(self, new_offset: Point):
        self._log.info("updated instrument offset to {}".format(new_offset))
        self._instrument_offset = new_offset

    @property
    def config(self) -> pipette_config.PipetteConfig:
        return self._config

    @property
    def model_offset(self):
        return self._model_offset

    def update_config_item(self, elem_name: str, elem_val: Any):
        self._log.info("updated config: {}={}".format(elem_name, elem_val))
        self._config = replace(self._config,
                               **{elem_name: elem_val})

    @property
    def name(self) -> str:
        return self._name

    @property
    def model(self) -> str:
        return self._model

    @property
    def pipette_id(self) -> Optional[str]:
        return self._pipette_id

    def critical_point(self, cp_override: CriticalPoint = None) -> Point:
        """
        The vector from the pipette's origin to its critical point. The
        critical point for a pipette is the end of the nozzle if no tip is
        attached, or the end of the tip if a tip is attached.

        If `cp_override` is specified and valid - so is either
        :py:attr:`CriticalPoint.NOZZLE` or :py:attr:`CriticalPoint.TIP` when
        we have a tip, or :py:attr:`CriticalPoint.XY_CENTER` - the specified
        critical point will be used.
        """
        if not self.has_tip or cp_override == CriticalPoint.NOZZLE:
            cp_type = CriticalPoint.NOZZLE
            tip_length = 0.0
        else:
            cp_type = CriticalPoint.TIP
            tip_length = self.current_tip_length
        if cp_override == CriticalPoint.XY_CENTER:
            mod_offset_xy = [0, 0, self.model_offset[2]]
            cp_type = CriticalPoint.XY_CENTER
        elif cp_override == CriticalPoint.FRONT_NOZZLE:
            mod_offset_xy = [
                0, -self.model_offset[1], self.model_offset[2]]
            cp_type = CriticalPoint.FRONT_NOZZLE
        else:
            mod_offset_xy = self.model_offset
        mod_and_tip = Point(mod_offset_xy[0],
                            mod_offset_xy[1],
                            mod_offset_xy[2] - tip_length)

        if enable_calibration_overhaul():
            instr = self._instrument_offset
        else:
            instr = self._instrument_offset._replace(z=0)

        cp = mod_and_tip + instr

        if self._log.isEnabledFor(logging.DEBUG):
            info_str = 'cp: {}{}: {} (from: '\
                .format(cp_type,
                        ' (from override)' if cp_override else '',
                        cp)
            info_str += 'model offset: {} + instrument offset: {}'\
                .format(mod_offset_xy, instr)
            info_str += ' - tip_length: {}'.format(tip_length)
            info_str += ')'
            self._log.debug(info_str)

        return cp

    @property
    def current_volume(self) -> float:
        """ The amount of liquid currently aspirated """
        return self._current_volume

    @property
    def current_tip_length(self) -> float:
        """ The length of the current tip attached (0.0 if no tip) """
        if enable_calibration_overhaul():
            return self._current_tip_length
        else:
            return (self._current_tip_length
                    - self._instrument_offset.z)

    @property
    def current_tiprack_diameter(self) -> float:
        """ The diameter of the current tip rack (0.0 if no tip) """
        return self._current_tiprack_diameter

    @current_tiprack_diameter.setter
    def current_tiprack_diameter(self, diameter: float):
        self._current_tiprack_diameter = diameter

    @property
    def aspirate_flow_rate(self) -> float:
        """ Current active flow rate (not config value)"""
        return self._aspirate_flow_rate

    @aspirate_flow_rate.setter
    def aspirate_flow_rate(self, new_flow_rate: float):
        assert new_flow_rate > 0
        self._aspirate_flow_rate = new_flow_rate

    @property
    def dispense_flow_rate(self) -> float:
        """ Current active flow rate (not config value)"""
        return self._dispense_flow_rate

    @dispense_flow_rate.setter
    def dispense_flow_rate(self, new_flow_rate: float):
        assert new_flow_rate > 0
        self._dispense_flow_rate = new_flow_rate

    @property
    def blow_out_flow_rate(self) -> float:
        """ Current active flow rate (not config value)"""
        return self._blow_out_flow_rate

    @blow_out_flow_rate.setter
    def blow_out_flow_rate(self, new_flow_rate: float):
        assert new_flow_rate > 0
        self._blow_out_flow_rate = new_flow_rate

    @property
    def working_volume(self) -> float:
        """ The working volume of the pipette """
        return self._working_volume

    @working_volume.setter
    def working_volume(self, tip_volume: float):
        """ The working volume is the current tip max volume """
        self._working_volume = min(self.config.max_volume, tip_volume)

    @property
    def available_volume(self) -> float:
        """ The amount of liquid possible to aspirate """
        return self.working_volume - self.current_volume

    def set_current_volume(self, new_volume: float):
        assert new_volume >= 0
        assert new_volume <= self.working_volume
        self._current_volume = new_volume

    def add_current_volume(self, volume_incr: float):
        assert self.ok_to_add_volume(volume_incr)
        self._current_volume += volume_incr

    def remove_current_volume(self, volume_incr: float):
        assert self._current_volume >= volume_incr
        self._current_volume -= volume_incr

    def ok_to_add_volume(self, volume_incr: float) -> bool:
        return self.current_volume + volume_incr <= self.working_volume

    def add_tip(self,
                tip_length: float) -> None:
        """
        Add a tip to the pipette for position tracking and validation
        (effectively updates the pipette's critical point)

        :param tip_length: a positive, non-zero float presenting the distance
            in Z from the end of the pipette nozzle to the end of the tip
        :return:
        """
        assert tip_length > 0.0, "tip_length must be greater than 0"
        assert not self.has_tip
        self._has_tip = True
        self._current_tip_length = tip_length

    def remove_tip(self) -> None:
        """
        Remove the tip from the pipette (effectively updates the pipette's
        critical point)
        """
        assert self.has_tip
        self._has_tip = False
        self._current_tip_length = 0.0

    @property
    def has_tip(self) -> bool:
        return self._has_tip

    def ul_per_mm(self, ul: float, action: 'UlPerMmAction') -> float:
        sequence = self._config.ul_per_mm[action]
        return pipette_config.piecewise_volume_conversion(ul, sequence)

    def __str__(self) -> str:
        return '{} current volume {}ul critical point: {} at {}'\
            .format(self._config.display_name,
                    self.current_volume,
                    'tip end' if self.has_tip else 'nozzle end',
                    0)

    def __repr__(self) -> str:
        return '<{}: {} {}>'.format(self.__class__.__name__,
                                    self._config.display_name,
                                    id(self))

    def as_dict(self) -> 'Pipette.DictType':
        config_dict = asdict(self.config)
        config_dict.update({'current_volume': self.current_volume,
                            'available_volume': self.available_volume,
                            'name': self.name,
                            'model': self.model,
                            'pipette_id': self.pipette_id,
                            'has_tip': self.has_tip,
                            'working_volume': self.working_volume,
                            'aspirate_flow_rate':  self.aspirate_flow_rate,
                            'dispense_flow_rate': self.dispense_flow_rate,
                            'blow_out_flow_rate': self.blow_out_flow_rate})
        return config_dict
