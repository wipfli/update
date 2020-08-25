import requests
import json
import os
import subprocess

def _execute(cmd='ls -lah'):
    try:
        subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return False
    
    return True

def _execute_get_output(cmd='ls -lah'):
    output = ''
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode().strip()
    except subprocess.CalledProcessError:
        return ''
    
    return output

def get_cmdline(path='/proc/cmdline'):
    return _execute_get_output('cat ' + path)

def get_passive(cmdline, p2='mmcblk0p2', p3='mmcblk0p3'):
    if p2 in cmdline:
        return p3
    if p3 in cmdline:
        return p2
    return ''

def mount_passive(partition='mmcblk0p2', path='/mnt/passive'):
    return _execute('mount ' + os.path.join('/dev/' + partition) + ' ' + path)

def get_current_version():
    current_version = ''
    # ...
    current_version = '1.0.0'
    return current_version

def get_releases(url='https://github.com'):
    releases = []

    try:
        r = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        return []
    except requests.exceptions.ConnectionError:
        return []

    if r.status_code != 200:
        return []

    try:
        releases = json.loads(r.text)
    except json.JSONDecodeError:
        return []

    return releases

def get_latest_release(releases={}, include_prereleases=False):
    for release in releases:
        if include_prereleases:
            return release
        else:
            if 'prerelease' not in release:
                return {}
            if not release['prerelease']:
                return release
    return {}

def download_file(url='https://github.com/', storage_path='download', progress_callback=lambda percentage: ()):
    local_filename = ''
    try:
        headers = requests.head(url).headers
        if 'Content-Length' not in headers:
            total_size = 1
        else:
            total_size = int(headers['Content-Length'])

        # https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
        local_filename = url.split('/')[-1]
        with requests.get(url, stream=True, timeout=10) as r:
            r.raise_for_status()
            chunk_i = 0
            last_percentage = 0
            progress_callback(last_percentage)
            with open(os.path.join(storage_path, local_filename), 'wb') as f:
                chunk_size = 8192
                for chunk in r.iter_content(chunk_size): 
                    f.write(chunk)
                    chunk_i += 1
                    percentage = min(int(100 * chunk_i * chunk_size / total_size), 100)
                    if percentage > last_percentage:
                        last_percentage = percentage
                        progress_callback(percentage)
    except requests.exceptions.Timeout:
        return ''
    except requests.exceptions.ConnectionError:
        return ''

    return local_filename

def download_assets(release={}, storage_path='download', progress_callback=lambda percentage: ()):
    if 'assets' not in release:
        return

    for asset in release['assets']:
        download_file(asset['browser_download_url'], storage_path, progress_callback)

def extract_xz(filename='download/rootfs.ext2.xz'):
    if _execute('unz -k ' + filename):
        return filename[:-3] # strip .xz extension
    else:
        return ''

def mount_image(filename='rootfs.ext2', path='/mnt/image'):
    return _execute('mount -o loop ' + filename + ' ' + path)

def copy_all(src='/mnt/image', dest='/mnt/passive'):
    return _execute('cp -Rp ' + os.path.join(src, '*') + ' ' + dest)

def remove_all(path='/mnt/passive'):
    return _execute('rm -rf ' + os.path.join(path, '*'))

def get_tar_md5sum(path='/mnt/passive'):
    output = _execute_get_output('tar c ' + path + ' | md5sum')
    if output == '':
        return ''
    parts = output.split(' ')
    if len(parts) > 0:
        return parts[0]
    else:
        return ''

def mount_boot(partition='mmcblk0p1', path='/mnt/boot'):
    return _execute('mount -t vfat ' + os.path.join('/dev/' + partition) + ' ' + path)

def flash_boot_select(partition='mmcblk0p2', filename='/mnt/boot/select.txt'):
    if partition == 'mmcblk0p2':
        return _execute('echo "cmdline=cmdline-p2.txt" > ' + filename)
    elif partition == 'mmcblk0p3':
        return _execute('echo "cmdline=cmdline-p3.txt" > ' + filename)
    else:
        return False





    

    
        
