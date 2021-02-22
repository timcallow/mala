from .snap import SNAP


def DescriptorInterface(params):
    """
    Return a DescriptorBase object that adheres to the parameters provided.

    Parameters
    ----------
    params : fesl.common.parameters.Parameters
        Parameters for which a DescriptorBase object is desired.
    """
    if params.descriptors.descriptor_type == 'SNAP':
        return SNAP(params)
    else:
        raise Exception("Unknown type of descriptor calculator requested.")
