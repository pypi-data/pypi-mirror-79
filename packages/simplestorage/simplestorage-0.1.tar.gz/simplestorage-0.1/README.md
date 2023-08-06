# simple-storage
Two ways simple interaction between cloud storage and local filesystem.

    pip install simplestorage

## Examples

### Path file/folder listing
    import simplestorage


    results = simplestorage.ls('/home/myuser/')

    print("######## DIRECTORIES  #########")
    for r in results:
        if r.is_folder:
            print(r.name)

    print("######## FILES #########")
    for r in results:
        if not r.is_folder:
            print(r.name)

you can use it with cloud too

    simplestorage.ls('gs://my-bucket/someprefix')

### File Saving to local/cloud
    import simplestorage

    simplestorage.save(data=b"some initial binary data: \x00\x01", uri="gs://mybucket/test/binary.bin")

for local just change the uri

    simplestorage.save(
        data=..., uri="/home/user/test/binary.bin")