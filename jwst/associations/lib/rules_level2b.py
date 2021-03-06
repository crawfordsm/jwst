"""Association Definitions: DMS Level2b product associations
"""
import logging

from jwst.associations.lib.constraint import Constraint
from jwst.associations.lib.dms_base import format_list
from jwst.associations.lib.rules_level2_base import *
from jwst.associations.lib.rules_level3_base import DMS_Level3_Base

__all__ = [
]

# Configure logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


# --------------------------------
# Start of the User-level rules
# --------------------------------
class Asn_Lv2Image(
        AsnMixin_Lv2Singleton,
        AsnMixin_Lv2Image,
        DMSLevel2bBase
):
    """Level2b Image"""

    def __init__(self, *args, **kwargs):

        # Setup constraints
        self.constraints = Constraint([
            Constraint_Base(),
            Constraint_Mode(),
            Constraint_Image_Science(),
        ])

        # Now check and continue initialization.
        super(Asn_Lv2Image, self).__init__(*args, **kwargs)


class Asn_Lv2ImageSpecial(
        AsnMixin_Lv2Special,
        AsnMixin_Lv2Singleton,
        AsnMixin_Lv2Image,
        DMSLevel2bBase
):
    """Level2b Image that are marked special
    Image exposures that are marked as backgrounds, imprints, etc.,
    still get 2b processing just as normal science. However, no other
    exposures should get included into the association.
    """

    def __init__(self, *args, **kwargs):

        # Setup constraints
        self.constraints = Constraint([
            Constraint_Base(),
            Constraint_Mode(),
            Constraint_Image_Science(),
            Constraint_Special(),
        ])

        # Now check and continue initialization.
        super(Asn_Lv2ImageSpecial, self).__init__(*args, **kwargs)


class Asn_Lv2ImageNonScience(
        AsnMixin_Lv2Special,
        AsnMixin_Lv2Singleton,
        AsnMixin_Lv2Image,
        DMSLevel2bBase
):
    """Level2b Image that are not science but get Level 2b processing"""

    def __init__(self, *args, **kwargs):

        # Setup constraints
        self.constraints = Constraint([
            Constraint_Base(),
            Constraint_Mode(),
            Constraint_Image_Nonscience(),
        ])

        # Now check and continue initialization.
        super(Asn_Lv2ImageNonScience, self).__init__(*args, **kwargs)


class Asn_Lv2FGS(
        AsnMixin_Lv2Singleton,
        AsnMixin_Lv2Image,
        DMSLevel2bBase
):
    """Level2b FGS"""

    def __init__(self, *args, **kwargs):

        # Setup constraints
        self.constraints = Constraint([
            Constraint_Base(),
            DMSAttrConstraint(
                name='exp_type',
                sources=['exp_type'],
                value=(
                    'fgs_image'
                    '|fgs_focus'
                ),
            )
        ])

        super(Asn_Lv2FGS, self).__init__(*args, **kwargs)


class Asn_Lv2Spec(
        AsnMixin_Lv2Singleton,
        AsnMixin_Lv2Spectral,
        DMSLevel2bBase
):
    """Level2b Spectra"""

    def __init__(self, *args, **kwargs):

        # Setup constraints
        self.constraints = Constraint([
            Constraint_Base(),
            Constraint_Mode(),
            Constraint_Spectral_Science()
        ])

        # Now check and continue initialization.
        super(Asn_Lv2Spec, self).__init__(*args, **kwargs)


class Asn_Lv2SpecSpecial(
        AsnMixin_Lv2Special,
        AsnMixin_Lv2Singleton,
        AsnMixin_Lv2Spectral,
        DMSLevel2bBase
):
    """Level2b Spectra that are marked special
    Spectral exposures that are marked as backgrounds, imprints, etc.,
    still get 2b processing just as normal science. However, no other
    exposures should get included into the association.
    """

    def __init__(self, *args, **kwargs):

        # Setup constraints
        self.constraints = Constraint([
            Constraint_Base(),
            Constraint_Mode(),
            Constraint_Spectral_Science(),
            Constraint_Special(),
        ])

        # Now check and continue initialization.
        super(Asn_Lv2SpecSpecial, self).__init__(*args, **kwargs)


class Asn_Lv2WFSS(
        AsnMixin_Lv2Singleton,
        AsnMixin_Lv2Spectral,
        DMSLevel2bBase
):
    """Level2b WFSS/GRISM exposures
    GRISM exposures require a source catalog from processing
    of the corresponding direct imagery.
    """

    def __init__(self, *args, **kwargs):

        self.constraints = Constraint([
            Constraint_Base(),
            Constraint_Mode(),
            DMSAttrConstraint(
                name='exp_type',
                sources=['exp_type'],
                value='nis_wfss',
            )
        ])

        super(Asn_Lv2WFSS, self).__init__(*args, **kwargs)

    def _init_hook(self, item):
        """Post-check and pre-add initialization"""
        super(Asn_Lv2WFSS, self)._init_hook(item)

        # Get the Level3 product name of this association.
        # Except for the grism component, it should be what
        # the Level3 direct image name is.
        lv3_direct_image_catalog = DMS_Level3_Base._dms_product_name(self) + '.ecsv'

        # Insert the needed catalog member
        member = {
            'expname': lv3_direct_image_catalog,
            'exptype': 'catalog'
        }
        members = self.current_product['members']
        members.append(member)

    def _get_opt_element(self):
        """Get string representation of the optical elements
        Returns
        -------
        opt_elem: str
            The Level3 Product name representation
            of the optical elements.
        Notes
        -----
        This is an override for the method in `DMSBaseMixin`.
        The second optical element, the grism, would never be part
        of the direct image Level3 name.
        """
        opt_elem = ''
        try:
            value = format_list(self.constraints['opt_elem'].found_values)
        except KeyError:
            pass
        else:
            if value not in _EMPTY and value != 'clear':
                opt_elem = value
        if opt_elem == '':
            opt_elem = 'clear'
        return opt_elem
