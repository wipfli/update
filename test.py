import update

passive_partition = update.get_passive_partition()

print(passive_partition)

def progress_callback(percentage):
    print(percentage)
    
update.download(url='https://github.com/wipfli/update/releases/download/v0.1.0/rootfs.ext2.xz', passive_partition=passive_partition, progress_callback=progress_callback, total_size=52807640)

print(update.get_checksum(passive_partition))

update.flash_boot_select(passive_partition)