typedef struct generic_resource_s {
    int value;
} generic_resource;

extern generic_resource *deflateInit(void);
extern int deflate(generic_resource *resource, int mode);

int generic_single_record_pointer_argument(void) {
    generic_resource *resource = deflateInit();
    if (resource == 0)
        return -1;
    return deflate(resource, 0);
}
