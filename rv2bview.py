import sys
import os
import os.path
import re
import pprint


class rv2bview:

    allsource = []

    def computeSource(self, source):
        result = {}
        pathfile = source.split("/")
        filename = pathfile[len(pathfile) - 1]

        matchearobase = re.findall("([@]+)", filename)
        result["source"] = source

        for matchseq in matchearobase:
            result["sequence"] = True
            result["padding"] = len(matchseq)
            newmatch = filename.replace("@", "")
            matchenumber = re.findall("[(0-9)]+-[(0-9)]+", newmatch)
            for matchn in matchenumber:
                numbers = matchn.split("-")
                result["start"] = numbers[0]
                result["end"] = numbers[1]

        return result

    def checkLine(self, line):
        regex = r"string movie = \"([a-zA-Z0-9_\-/.@]+)\""
        matches = re.findall(regex, line)

        for match in matches:
            self.allsource.append(self.computeSource(match))

    def isSequence(self, source):
        """

        """
        if 'sequence' in source:
            return True
        else:
            return False

    def getFilenameSequenceBview(self, source):
        """
                return the well formatted source bview for a sequence filename
                @param:  source dictonnary description of the sequence ...
        """
        padding = source["padding"]
        str2replace = ("@" * padding)[0:padding]
        tmpsource = source["source"].replace("%s-%s" % (source["start"], source["end"]), "")
        return tmpsource.replace(str2replace, "["+source["start"].rjust(padding, '0')+"-"+source["end"].rjust(padding, '0')+"]")

    def convertToBview(self):
        for s in self.allsource:
            if self.isSequence(s):
                self.getFilenameSequenceBview(s)
                print """
        newSequence(
                    file_name = "%s",
                     begin =%s,
                     end = %s,
                     selected = ON
            );
        """ % ( self.getFilenameSequenceBview(s), s["start"], s["end"] )

            else:
                print """
        newSequence(
              file_name = "%s",
                      selected = ON
            );
        """ % ( s["source"] )


# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.


r2b = rv2bview()
with open(sys.argv[1], "r") as f:
    text = f.read()
    r2b.checkLine(text)
    r2b.convertToBview()