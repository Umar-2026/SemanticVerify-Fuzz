from .resource_state import ResourceState



def apply_effect(resource, effect):

    if effect is None:
        return


    effect = effect.lower()


    if "allocate" in effect:

        resource.allocate(
            owner="api"
        )


    elif "release" in effect:

        resource.release()
