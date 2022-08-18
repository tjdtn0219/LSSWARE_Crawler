
from scrapy.selector import Selector
from Crawler.items import ReleaseItem
from datetime import datetime
import scrapy

class TestClass:
    Version_heads = ["version", "name", "release", "series", "general availability"]
    Date_heads = ["first release", "release date", "date of issue", "latest release"]

    def listToString(str_list):
        result = ""
        for s in str_list:
            result += s.strip() + " "
        return result.strip()

    def isStrEmpty(str):
        if str is None:
            return False
        
        else:
            if str.strip() == "":
                return False
            else:
                return True

    def parsing_version_in_row(table_row, version_col_idx):

        idx = version_col_idx[0] + 1
        if TestClass.isStrEmpty(Selector(text=table_row).xpath('.//tr/*[' + str(idx) + ']/text()').get()):
            version = Selector(text=table_row).xpath('.//tr/*[' + str(idx) + ']/text()').get().strip()
        elif TestClass.isStrEmpty(Selector(text=table_row).xpath('.//tr/*[' + str(idx) + ']/a/text()').get()):
            version = Selector(text=table_row).xpath('.//tr/*[' + str(idx) + ']/a/text()').get().strip()
        elif TestClass.isStrEmpty(Selector(text=table_row).xpath('.//tr/*[' + str(idx) + ']/@data-sort-value').get()):
            version = Selector(text=table_row).xpath('.//tr/*[' + str(idx) + ']/@data-sort-value').get().strip()
        else:
            version = None
        
        return version

    def parsing_date_in_row(table_row, date_col_idx, rowspan_is_flag, rowspan_flag):

        if rowspan_is_flag:
            print("TAG")
            if rowspan_flag:
                idx = date_col_idx[0] + 1
            else:
                idx = date_col_idx[0]
        else:
            idx = date_col_idx[0] + 1
        print("idx : "+ str(idx))
        if TestClass.isStrEmpty(Selector(text=table_row).xpath('.//tr/*[' + str(idx) + ']/text()').get()):
            date = Selector(text=table_row).xpath('.//tr/*[' + str(idx) + ']/text()').get().strip()
        else:
            date = None
            if len(date_col_idx) > 1:
                if TestClass.isStrEmpty(Selector(text=table_row).xpath('.//tr/*[' + str(idx) + ']/text()').get()):
                    date = Selector(text=table_row).xpath('.//tr/*[' + str(idx) + ']/text()').get().strip()

        return date

    def find_col_idx(table_heads, str_list):
        col_idx = []
        for i, head in enumerate(table_heads):
            head_list = Selector(text=head).xpath('.//text()').getall()
            head = TestClass.listToString(head_list)
            print(head)
            for str in str_list:
                if str in head.lower():
                    col_idx.append(i)

        return col_idx

    def delete_table_heads(table_rows):                
        while len(Selector(text=table_rows[0]).xpath('.//td').getall()) == 0:
            del table_rows[0]

    def select_tables(tables):
        table_list = []

        for table in tables:
            table_rows = Selector(text=table).xpath('.//tbody/tr').getall()
            if len(table_rows) != 1:
                table_heads = Selector(text=table).xpath('.//tbody/tr[1]/th').getall()
                version_col_idx = TestClass.find_col_idx(table_heads, TestClass.Version_heads)
                date_col_idx = TestClass.find_col_idx(table_heads, TestClass.Date_heads)
                if len(version_col_idx) > 0 and len(date_col_idx) > 0:
                    table_list.append(table)
                elif (len(version_col_idx) > 0 or len(date_col_idx) > 0) and len(table_rows) == 2:
                    table_list.append(table)
        return table_list
                    

    def is_rowspan(table_rows, date_col_idx):
        is_flag = False
        for table_row in table_rows:
            for i, col in enumerate(Selector(text=table_row).xpath('.//tr/*').getall()):
                # i is col index of row span

                if Selector(text=col).xpath('.//td/@rowspan').get():
                    print(date_col_idx[0])
                    print(i)
                    if i < date_col_idx[0]:
                        # row span is located before date column
                        is_flag = True

        return is_flag

    def is_horizon_table(table):
        table_rows = Selector(text=table).xpath('.//tbody/tr').getall()
        if len(table_rows) == 2:
            return True
        else:
            return False

    def parsing_table(table):
        table_rows = Selector(text=table).xpath('.//tbody/tr').getall()

        if len(table_rows) > 2:
            # This is verticle table
            for item in TestClass.parsing_verticle_table(table):
                yield item
        else:
            for item in TestClass.parsing_horizon_table(table):
                yield item

    def parsing_verticle_table(table):          
        release = ReleaseItem()

        table_rows = Selector(text=table).xpath('.//tbody/tr').getall()
        table_heads = Selector(text=table_rows[0]).xpath('.//th').getall()
        
        version_col_idx = TestClass.find_col_idx(table_heads, TestClass.Version_heads)
        date_col_idx = TestClass.find_col_idx(table_heads, TestClass.Date_heads)

        print("===========")
        print(date_col_idx)

        TestClass.delete_table_heads(table_rows)


        rowspan_is_flag = TestClass.is_rowspan(table_rows, date_col_idx)

        for table_row in table_rows:
            rowspan_flag = False

            if rowspan_is_flag and Selector(text=table_row).xpath('.//tr/*/@rowspan').get():
                rowspan_flag = True     

            version = TestClass.parsing_version_in_row(table_row, version_col_idx)
            date = TestClass.parsing_date_in_row(table_row, date_col_idx, rowspan_is_flag, rowspan_flag)

            if version is not None and date is not None: 
                release['Version'] = version
                release['Date'] = TestClass.date_to_str(date.strip())
                # release['Date'] = date.replace('\u00a0', " ")
                yield release

    def parsing_horizon_table(table):            
        release = ReleaseItem()

        table_rows = Selector(text=table).xpath('.//tbody/tr').getall()
        
        col_1 = Selector(text=table_rows[0]).xpath('.//th/text()').getall()
        col_2 = Selector(text=table_rows[1]).xpath('.//td/text()').getall()

        assert len(col_1) == len(col_2)

        for i in range(1, len(col_1)):
            release['Version'] = col_1[i].strip()
            release['Date'] = TestClass.date_to_str(col_2[i].strip())
            yield release


    def select_catalog(response):
        # select a proper ul tag and return html codes
        # if webpage headlines change, you should modify "headline_str"
        headline_str = ["code names", "release history", "application server versions"]

        idx_list = []
        items = response.xpath('//div[@class="mw-parser-output"]/*').getall()

        for i, item in enumerate(items):
            headline = Selector(text=item).xpath('.//*/span[@class="mw-headline"]/text()').get()
            if headline:
                for str in headline_str:
                    if str in headline.strip().lower():
                        idx_list.append(i)

        for i in idx_list:
            for j in range(1,5):
                if Selector(text=items[i+j]).xpath('.//li').get():
                    return items[i+j]
        return None

    def parsing_catalog(response):
        release = ReleaseItem()

        catalog = TestClass.select_catalog(response)
        rows = Selector(text=catalog).xpath('.//li/text()').getall()
        for row in rows:
            row_split = row.split('-', 1)
            if len(row_split) == 2:
                date = TestClass.date_to_str(row_split[1].strip())
                if date:
                    version = row_split[0].strip()
                else:
                    version = row
            else:
                version = row
                date = None

            release['Version'] = version
            release['Date'] = date
            yield release


    def date_to_str(str_date):
        list_formats = [
            "%B %d, %Y", "%d %B %Y", "%Y-%m-%d", "%B %Y", "%Y/%m/%d", "%b %Y", "%d/%m/%Y",
            "%m/%d/%Y", "%Y.%m", "%B\u00a0%d, %Y", "%d\u00a0%B %Y", "%Y"
        ]
        for format in list_formats:
            try:
                date_obj = datetime.strptime(str_date, format)
                return date_obj.strftime("%Y/%m/%d")

            except ValueError:
                continue
        return None
