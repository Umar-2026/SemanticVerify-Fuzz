typedef struct generic_resource_s {
    int value;
} generic_resource;

extern int deflate(generic_resource *resource, int mode);

int generic_parameter_alias_boundary(generic_resource *resource) {
    return deflate(resource, 0);
}
