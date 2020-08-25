import update

url = 'https://api.github.com/repos/wipfli/test/releases'
prerelease = True

#releases = [{'name': 'first', 'prerelease': True}, {'name': 'second', 'prerelease': False}]

#releases = update.get_releases(url)

#release = update.get_latest_release(releases, include_prereleases=True)

def progress_callback(percentage):
    print(percentage)

#update.download_assets(release, 'download/', progress_callback)


#update.download_file('https://dl.influxdata.com/influxdb/releases/influxdb-1.8.2_linux_amd64.tar.gz', 'download', progress_callback)

#print(update.extract_xz('download/rootfs.ext2.xz'))

#print(update.remove_all(path='download/new/'))

#print(update.copy_all(src='download/influxdb-1.8.2-1/', dest='download/new/'))

#print(update.get_tar_md5sum('download/'))

print(update.flash_boot_select(partition='mmclbk0p2', filename='hallo.txt'))