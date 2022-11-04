from specifications.utilities.Recording_сharacteristics import RecordingUniqueValues


def uploading_csv_file(instance):
    byte_content = instance.uploading_csv_file.open().read()
    content = byte_content.decode()
    write_specs(content, instance)
    instance.uploading_csv_file.delete()


def write_specs(content, props):
    content = content.replace('\ufeff', '')
    content = content.split('\r\n')
    list_spec = [[x.split(';')[0], x.split(';')[1]] for x in content if x]
    d = dict(list_spec)
    _keys, _values = list(d.keys()), list(d.values())
    product_and_spec = {props.name: list_spec, }
    _ = {'spec_list': _keys, 'value_list': _values, 'product': product_and_spec, 'product_name': props.name}
    obj = RecordingUniqueValues(**_)

    obj.spec()
    obj.value()
    obj.write()
