""" The MIT License (MIT)

Copyright (c) 2016 DavidJBianco

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. """

import re


def parse_cef(str_input):
    values = dict()
    header_re = r"((CEF:\d+)([^=\\]+\|){,7})(.*)"
    res = re.search(header_re, str_input)

    if res:
        header = res.group(1)
        extension = res.group(4)

        spl = re.split(r"(?<!\\)\|", header)

        values["Vendor"] = spl[1]
        values["Product"] = spl[2]
        values["Version"] = spl[3]
        values["SignatureID"] = spl[4]
        values["Name"] = spl[5]
        if len(spl) > 6:
            values["Severity"] = spl[6]

        cef_start = spl[0].find("CEF")
        if cef_start == -1:
            return None
        version = spl[0][cef_start:].split(":")[1]
        values["CEFVersion"] = version

        spl = re.findall(r"([^=\s]+)=((?:[\\]=|[^=])+)(?:\s|$)", extension)
        for i in spl:
            values[i[0]] = i[1]

        for key in list(values.keys()):
            if key[-5:] == "Label":
                customlabel = key[:-5]
                for customfield in list(values.keys()):
                    if customfield == customlabel:
                        values[values[key]] = values[customfield]
                        del values[customfield]
                        del values[key]
    else:
        return None
    return values
