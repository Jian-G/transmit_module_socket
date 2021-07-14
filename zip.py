import os,time
import zipfile
import gzip,shutil
import lzma
import bz2
import tarfile

def zip_by_zipfile(input):
    start_time = time.time()
    zip = zipfile.ZipFile(input + ".zip", "w", zipfile.ZIP_DEFLATED)
    zip.write(input)
    zip.close()
    end_time = time.time()
    return round(end_time - start_time, 2)


def unzip_by_zipfile(input):
    start_time = time.time()
    zip = zipfile.ZipFile(input, 'r')
    for filename in zip.namelist():
        data = zip.read(filename)
        file = open(filename,'w+b')
        file.write(data)
        file.close()
    end_time = time.time()
    return round(end_time - start_time, 2)

def zip_by_gzip(input):
    start_time = time.time()
    with open(input, 'rb') as fin:
        with gzip.open(input + ".gz", 'wb') as fout:
            shutil.copyfileobj(fin, fout)
    end_time = time.time()
    return round(end_time - start_time, 2)

def unzip_by_gzip(input):
    start_time = time.time()
    with gzip.open(input, 'rb') as fin:
        with open(input.rsplit(".",1)[0], 'wb') as fout:
            shutil.copyfileobj(fin, fout)
    end_time = time.time()
    return round(end_time - start_time, 2) 

def zip_by_lzma(input):
    start_time = time.time()
    with open(input, 'rb') as fin:
        with lzma.open(input + ".xz", 'wb') as fout:
            shutil.copyfileobj(fin, fout)
    end_time = time.time()
    return round(end_time - start_time, 2)

def unzip_by_lzma(input):
    start_time = time.time()
    with lzma.open(input, 'rb') as fin:
        with open(input.rsplit(".",1)[0], 'wb') as fout:
            shutil.copyfileobj(fin, fout)
    end_time = time.time()
    return round(end_time - start_time, 2)  

def zip_by_bz2(input):
    start_time = time.time()
    with open(input, 'rb') as fin:
        with bz2.open(input + ".bz2", 'wb') as fout:
            shutil.copyfileobj(fin, fout)
    end_time = time.time()
    return round(end_time - start_time, 2)

def unzip_by_bz2(input):
    start_time = time.time()
    with bz2.open(input, 'rb') as fin:
        with open(input.rsplit(".",1)[0], 'wb') as fout:
            shutil.copyfileobj(fin, fout)
    end_time = time.time()
    return round(end_time - start_time, 2) 

def zip_by_tarfile(input):
    start_time = time.time()
    with tarfile.open(input + ".tar.gz", 'w:gz') as fout:
        fout.add(input)
    end_time = time.time()
    return round(end_time - start_time, 2)

def unzip_by_tarfile(input):
    start_time = time.time()
    with tarfile.open(input, 'r:gz') as fin:
        fin.extract(input.rsplit(".",2)[0], './')
    end_time = time.time()
    return round(end_time - start_time, 2) 

if __name__ == "__main__":
    filename = "recovery.pdf"
    originsize = round(os.path.getsize(filename)/1000/1000, 2)
    print("Filename : {}\tOrigin Size : {} MB".format(filename, originsize))


    print("**** Info for zip ****")

    gzip_ziptime = zip_by_gzip(filename)
    gzip_zipsize = round(os.path.getsize(filename + ".gz")/1000/1000, 2)
    print("Gzip library zip time : {}s".format(gzip_ziptime))
    print("Gzip library zip size : {} MB".format(gzip_zipsize))
    print("Gzip library zip ratio: {}".format(round(gzip_zipsize/originsize, 2)))


    bz2_ziptime = zip_by_bz2(filename)
    bz2_zipsize = round(os.path.getsize(filename + ".bz2")/1000/1000, 2)
    print("Bz2 library zip time : {}s".format(bz2_ziptime))
    print("Bz2 library zip size : {} MB".format(bz2_zipsize))
    print("Bz2 library zip ratio: {}".format(round(bz2_zipsize/originsize, 2)))

    lzma_ziptime = zip_by_lzma(filename)
    lzma_zipsize = round(os.path.getsize(filename + ".xz")/1000/1000, 2)
    print("Lzma library zip time : {}s".format(lzma_ziptime))
    print("Lzma library zip size : {} MB".format(lzma_zipsize))
    print("Lzma library zip ratio: {}".format(round(lzma_zipsize/originsize, 2)))

    zipfile_ziptime = zip_by_zipfile(filename)
    zipfile_zipsize = round(os.path.getsize(filename + ".zip")/1000/1000, 2)
    print("Zipfile library zip time : {}s".format(zipfile_ziptime))
    print("Zipfile library zip size : {} MB".format(zipfile_zipsize))
    print("Zipfile library zip ratio: {}".format(round(zipfile_zipsize/originsize, 2)))

    tarfile_ziptime = zip_by_tarfile(filename)
    tarfile_zipsize = round(os.path.getsize(filename + ".tar.gz")/1000/1000, 2)
    print("Tarfile library zip time : {}s".format(tarfile_ziptime))
    print("Tarfile library zip size : {} MB".format(tarfile_zipsize))
    print("Tarfile library zip ratio: {}".format(round(tarfile_zipsize/originsize, 2)))

    print("**** Info for unzip ****")
    gzip_unziptime = unzip_by_gzip(filename + ".gz")
    print("Gzip library unzip time : {}s".format(gzip_unziptime))
   
    bz2_unziptime = unzip_by_bz2(filename + ".bz2")
    print("Bz2 library unzip time : {}s".format(bz2_unziptime))

    lzma_unziptime = unzip_by_lzma(filename + ".xz")
    print("Lzma library unzip time : {}s".format(lzma_unziptime))

    zipfile_unziptime = unzip_by_zipfile(filename + ".zip")
    print("Zipfile library unzip time : {}s".format(zipfile_unziptime))

    tarfile_unziptime = unzip_by_tarfile(filename + ".tar.gz")
    print("Tarfile library unzip time : {}s".format(tarfile_unziptime))

