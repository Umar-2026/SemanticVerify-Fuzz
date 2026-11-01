typedef struct generic_resource_s {
    int value;
} generic_resource;

extern int deflate(generic_resource *left, generic_resource *right);

int generic_ambiguous_multi_resource(void) {
    generic_resource left = {0};
    generic_resource right = {0};
    return deflate(&left, &right);
}
