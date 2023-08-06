#!/usr/bin/python3


import os
import sys
import re

import jk_argparsing
import jk_pwdgen







ap = jk_argparsing.ArgsParser("pwdgen [options]", "Generate strong passwords.")

ap.optionDataDefaults.set("help", False)
ap.optionDataDefaults.set("n", 1)
ap.optionDataDefaults.set("length", 24)
ap.optionDataDefaults.set("minNumberOfNumericChars", 2)
ap.optionDataDefaults.set("numberOfSpecialChars", 3)
ap.optionDataDefaults.set("prohibitedChars", "0l")

ap.createOption("h", "help", "Display this help text.").onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("help", True)

ap.createOption("n", None, "Number of passwords to generate. (Default: 1)").expectInt32("n", minValue=1).onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("n", argOptionArguments[0])
ap.createOption("l", "length", "Length of password to generate. (Default: 24)").expectInt32("n", minValue=3).onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("length", argOptionArguments[0])
ap.createOption(None, "minNumberOfNumericChars", "Minimum number of numeric characters. (Default: 2)").expectInt32("n", minValue=0).onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("minNumberOfNumericChars", argOptionArguments[0])
ap.createOption(None, "numberOfSpecialChars", "Minimum number of special characters. (Default: 3)").expectInt32("n", minValue=0).onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("numberOfSpecialChars", argOptionArguments[0])
ap.createOption(None, "prohibitedChars", "Prohibites characters. (Default: \"0l\")").expectString("s", minLength=0).onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("prohibitedChars", argOptionArguments[0])

ap.createAuthor("Jürgen Knauth", "jk@binary-overflow.de")
ap.setLicense("Apache", YEAR = 2020, COPYRIGHTHOLDER = "Jürgen Knauth")

ap.createReturnCode(0, "Everything is okay.")
ap.createReturnCode(1, "An error occurred.")

ap.addDescriptionChapter(None, [
	"This tool assists in the generation of strong passwords. Generation is based on the Python random number generator random.Random. According to the Python "
	"documentation this RNG is based on Mersenne Twister and os.urandom(), so it should provide sufficient randomness for password generation."
	,
	"This tool checks that passwords generated are of sufficient qualty. Depending on options set if invoked it ensures that passwords will have the "
	"correct number of special characters as well as enough numeric characters."
	,
	"In order to use this password generation tool just run it. On each run it will generate one or more passwords (depending on arguments specified). "
	"All passwords are printed to STDOUT line by line."
])




parsedArgs = ap.parse()
#parsedArgs.dump()

if parsedArgs.optionData["help"]:
	ap.showHelp()
	sys.exit(0)




pwdGen = jk_pwdgen.PasswordGenerator(
	length = parsedArgs.optionData["length"],
	minNumberOfNumericChars = parsedArgs.optionData["minNumberOfNumericChars"],
	numberOfSpecialChars = parsedArgs.optionData["numberOfSpecialChars"],
	prohibitedChars = parsedArgs.optionData["prohibitedChars"],
)

for i in range(0, parsedArgs.optionData["n"]):
	print(pwdGen.generate())

bSuccess = True




sys.exit(0 if bSuccess else 1)










