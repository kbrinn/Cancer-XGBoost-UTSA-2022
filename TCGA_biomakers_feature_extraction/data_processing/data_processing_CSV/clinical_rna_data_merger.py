import os

def table_join(transpose_file, patiant_file, base_dir, OverAll):
    os.chdir('/'.join(transpose_file.split('/')[:-1]))
    print(os.getcwd())
    fileEndName = patiant_file.split('/')[2].split('-')[1] + ".csv"

    with open(transpose_file,'r') as file:
        transposeData = [line.replace('\n','').split(',') for index ,line in enumerate(file) if index != 0]

    with open(patiant_file,'r') as file:
        patiantData = [line.replace('\n','').split(',') if index != 0 else line.replace('\n','').split(',') for index ,line in enumerate(file)]
    newData = [patiantData[0] + transposeData[0][1:]]

    for x in patiantData:
        for y in transposeData:
            if x[0] == y[0]:
                newData.append(x + y[1:])
                break
    container = []
    with open(fileEndName,'w') as file:
        for index, line in enumerate(newData):
            if index == 0:
                print("Collumn Length of " + fileEndName + ":", len(line))
            print(','.join(line), file=file, end='\n')
            if index != 0 or OverAll == 0:
                container.append(','.join(line))
    os.chdir(base_dir)
    return container

def filenames():
    baseDir = os.getcwd() + '/dataset_preprocessed/'
    files = []
    for dir in os.walk(os.curdir):
        for fileListing in dir:
            patiant_file = ""
            transpose_file = ""
            for filename in fileListing:
                if 'transposed' in filename:
                    transpose_file = filename
                if 'patient' in filename:
                    patiant_file = filename
            if patiant_file and transpose_file:
                files.append([patiant_file, transpose_file])

    newFileNames = []
    for file in files:
        patiantFile = baseDir + "TCGA-" + file[0].split('_')[0] + "/" + file[0]
        transposefile = baseDir + "TCGA-" + file[1].split('_')[1] + "/" + file[1]
        newFileNames.append([transposefile, patiantFile,])
    return newFileNames

def main():

    print(os.listdir())
    print(os.getcwd())
    files = filenames()
    overAllFile = []
    for items in files:
        overAllFile += table_join(items[0], items[1],os.getcwd(), len(overAllFile))

    with open("TCGA-Merge.csv",'w') as file:
        for line in overAllFile:
            print(line,file=file)


if __name__ =='__main__':
    main()