typedef struct generic_resource_s {
    int value;
} generic_resource;

extern generic_resource *deflateInit(void);

int generic_return_pointer_acquisition(void) {
    generic_resource *resource = deflateInit();
    return resource == 0;
}
