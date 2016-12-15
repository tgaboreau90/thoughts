import csv

class LocalCsv:
    def __init__(self, fileName = None, directory = None):
        self.fileName = fileName
        if directory:
            self.directory = directory
            self.fileString = '%s\\%s' % (directory, fileName)
        else:
            self.directory = None
            self.fileString = '%s' % (fileName)
    dict = {}
    list = []
  
    def OpenToDict(self, index, skiplines = 0):
        skippedlines = 0
        print 'importing %s' % self.fileName
        """opens csv, converts to dictionary where 'index' field is the key and the value is another dictionary containing every other field"""
        with open(self.fileString, 'rb') as f:
            reader=csv.reader(f)
            while skippedlines < skiplines:
                reader.next()
                skippedlines += 1
            headings = reader.next()
            heading_nums={}
            for i, v in enumerate(headings):
                heading_nums[v]=i
            fields = [heading for heading in headings if heading <> index]
            file_dictionary = {}
            for row in reader:
                file_dictionary[row[heading_nums[index]]]={}
                for field in fields:
                    file_dictionary[row[heading_nums[index]]][field]=row[heading_nums[field]]
        return file_dictionary
    
    def OpenToDictList(self, skiplines = 0):
        skippedlines = 0
        with open(self.fileString, 'rb') as f:
            reader=csv.reader(f)
            while skippedlines < skiplines:
                reader.next()
                skippedlines += 1
            headings = reader.next()
            file_list = []
            for row in reader:
                file_list.append({headings[i]:v for i, v in enumerate(row)})
        return file_list
    
    def DictListToCsv(self, Data, FileName, FieldNames = None):
        if FieldNames == 'phocasdefault':
            f = open('columns.txt', 'r')
            FieldNames = f.next().split(',')[:-1]
        elif not FieldNames:
             FieldNames = [k for k in Data[0]]
        with open(FileName, 'w') as f:
            writer = csv.DictWriter(f, fieldnames = FieldNames, dialect = 'excel', delimiter=',', lineterminator='\n')
            writer.writeheader()
            writer.writerows(Data)
    
    def GetCols(self, skiplines = 0):
        skippedlines = 0
        with open(self.fileString, 'rb') as f:
            reader=csv.reader(f)
            while skippedlines < skiplines:
                reader.next()
                skippedlines += 1
            return reader.next()
        
    

class LocalXlsx:
    def __init__(self):
        pass
    
    def SaveXlsx(self, Filename, Data, SheetTitle = 'Auto-Sheet1'):
        wb = Workbook()
        ws = wb.active
        ws.title = SheetTitle
        r, c = 1,1
        if type(Data) == list:
            headersDone = False
            headers = [h for h in Data[0]]
            for line in Data:
                if not headersDone:
                    for h in headers:
                        ws.cell(row = r, column = c).value = h
                        c +=1
                    r+=1
                    c=1
                    headersDone = True 
                else:
                    pass
                for k, v in line.iteritems():
                    ws.cell(row = r, column = c).value = v
                    c+=1
                r+=1
                c=1
        wb.save(Filename)
            
            
class DataSource:
    "Takes an ODBC connstring as an argument" 
    def __init__(self, connString = None, host = None, user = None, passwd = None, db = None):
        self.connString = connString
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
    
    def QuerySingleFigure(self, sqlString):
        conn = pyodbc.connect(self.connString)
        cursor = conn.cursor()
        cursor.execute(sqlString)
        return cursor.fetchone()[0]
        
    def Query(self, sqlString, indexCol = None):
        """Connects to the the datasource using self.connString, executes the query defined in the sqlString argument. 
        indexCol argument can be used to specify which field of the query is the primary lookup field. Depending on index argument the function returns either:
            1) if no index field is given then data object returned is like [{a' : 'foo', 'b' : 1}, {'a' : 'bar', 'b' : 2}] 
               (list of dictionaries where each dictionary represents a row returned by the query)
            2) if index argument is given then object returned is like {'foo': {'b' : 1}, 'bar': {'b' : 2}} where 'a' is the index field and 'foo' and 'bar' are the values from field 'a'
               (Dictionary where each value from index field is a key, and the value stored under that key is another dictionary which represents that row from the query)
               EACH VALUE IN INDEX COLUMN MUST BE UNIQUE!! - DUPLICATE VALUES IN INDEX COLUMN WILL CAUSE KEYS TO BE OVERWRITTEN AND DATA TO BE LOST!!"""
        conn = pyodbc.connect(self.connString)
        cursor = conn.cursor()
        cursor.execute(sqlString)
        cols = [col[0] for col in cursor.description]
        row = 'start'
        if indexCol:
            indexPos = cols.index(indexCol)
            data = {}
            while row:
                row = cursor.fetchone()
                if row != None:
                    key = None
                    key = row[indexPos]
                    data[key]={}
                    data[key] = {col:row[cols.index(col)] for col in cols if col <> indexCol}
        else:
            data = []
            while row:
                row = cursor.fetchone()
                if row != None:
                    rowData = {col:row[cols.index(col)] for col in cols}
                    data.append(rowData)
        conn.close()
        return data

    def MySQLQuery(self, sqlString):
        conn = pymysql.connect(host=self.host, port=3306, user=self.user, passwd=self.passwd, db=self.db)
        cursor = conn.cursor()
        cursor.execute(sqlString)
        cols = [col[0] for col in cursor.description]
        row = 'start'
        data = []
        while row:
            row = cursor.fetchone()
            if row != None:
                rowData = {col:row[cols.index(col)] for col in cols}
                data.append(rowData)
        cursor.close()
        conn.close()
        return data
            
    def ExecQuery(self, sqlString):
        conn = pyodbc.connect(self.connString)
        cursor = conn.cursor()
        cursor.execute(sqlString)
        cursor.commit()
        conn.close()
        
    def InsertLine(self, table, columns, values):
        conn = pyodbc.connect(self.connString)
        cursor = conn.cursor()
        cursor.execute("insert into %s%s values %s" % (table, columns, values))
        conn.commit()
        
    def MakeValuesString(self, values):
        added = 0
        output = '('
        while added < len(values):
            if type(values[added]) in (float, int, long):
                output = output + str(values[added])
            elif type(values[added]) == str:
                output = output + "'" + values[added] + "'"
            added += 1
            if added < len(values):
                output = output + ','
        output = output + ')'
        return output
         
        
ConnStrings = {
               'solvitt'                : 'DSN=Solvitt;Description=Solvitt;UID=phocas;PWD=phocas247;APP=Microsoft Office 2010;WSID=P3303386',
               'magento_copy'           : 'DSN=Magento_Copy; Database = magento_enterprise;',
               'backoffice_copy'        : 'DSN=Trueshopping_Copy; Database = trueshopping_copy;',
               'backoffice_live'        : 'DSN=TrueshoppingLive;',
               'magento_live'           : 'DSN=Magento_Copy; Database = magento_enterprise;',
               'backoffice_views'       : 'DSN=Trueshopping_Views;',
               'magento_views'          : 'DSN=Magento_Views;',
               'phocas'                 : 'DRIVER={SQL Server};SERVER=.;DATABASE=Phocas_TG;UID=sa;PWD=P@ssw0rd'
               
               }


def QueryToCsv(ConnString, SqlString, FileName, FieldNames = None):
    Data = DataSource(ConnString).Query(SqlString)
    c = LocalCsv()
    c.DictListToCsv(Data, FileName, FieldNames)
    
def MySQLQueryToCsv(host, user, passwd, db, SqlString, FileName, FieldNames = None):
    Data = DataSource(host = host, user = user, passwd = passwd, db = db).MySQLQuery(SqlString)
    c = LocalCsv()
    c.DictListToCsv(Data, FileName, FieldNames)

def Chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]
        
def Stringify(listobj):
    QueryString = '('
    for thing in listobj:
        QueryString = QueryString + "'" + str(thing) + "' ,"
    QueryString = '%s)' % QueryString[:-2]
    return QueryString   


def jsonify(data, dimensions, metrics, struc = {}):
    for row in data:
        pointer = struc
        if dimensions:
            for dimension in dimensions:
                pointer.setdefault(row[dimension], {})
                pointer = pointer[row[dimension]]
            for metric in metrics:
                pointer.setdefault(metric, 0.0)
                pointer[metric] += float(row[metric])
        else:
            pointer.setdefault('total', {})
            pointer = pointer['total']
            for metric in metrics:
                pointer.setdefault(metric, 0.0)
                pointer[metric] += float(row[metric])    
    return struc

def jsonifyClassInstances(instances, dimensions, metrics, struc = {}):
    for i in instances:
        pointer = struc
        if dimensions:
            for dimension in dimensions:
                pointer.setdefault(getattr(i, dimension), {})
                pointer = pointer[getattr(i, dimension)]
            for metric in metrics:
                pointer.setdefault(metric, 0.0)
                pointer[metric] += float(getattr(i, metric))
        else:
            pointer.setdefault('total', {})
            pointer = pointer['total']
            for metric in metrics:
                pointer.setdefault(metric, 0.0)
                pointer[metric] += float(getattr(i, metric))    
    return struc
       

    

 
