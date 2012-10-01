#Sublime: XMLLint

A plugin for Sublime Text 2 using LibXML2 for XML Validation capabilities.
- Based off of sublime-jslint plugin by fbzhong

##Version:

- Initial Public Beta
-- 0.0.8
-- Use at your own risk, fork at your leisure

#Note:

This was a project I took on personally so that I could use XML validation in addition to Sublime's excellent syntax highlighting. Since there was no such plugin out at the time, I decided to build my own to validate the XML. Since I will not be developing in an XML environment much longer, it is not complete, I cannot guarantee that your computer won't explode, and I've only tested in Windows 7 64-bit with Sublime Text 2 64-bit. I had done research and made plans to migrate from LibXML2 to a more Pythonic library, and I have documented future ideas below for anyone who wants to build off of this project.

##Future plans:

- Switch from LibXML2 to Python lxml module (or cElementTree/elementTree/etc) to aid in:

    1. Loading Schema/DTD into memory in order to validate after losing internet connection
    2. Make plugin location-aware, tracking what node it's in for auto-completion, what line errors are on, etc
- Create more user friendly panel information
- Validate well-formedness even if no DTD is found

#License:

Code within the libxml folder of this project is licensed under the MIT license. <http://opensource.org/licenses/mit-license.php>

All lines of code, excluding those lines in the libxml directory of this project, that are identical to lines within the sublime-jslint plugin by fbzhong at commit ee0a8c2f8ba130807d8f9c604558d4e73c638fcb are governed by the following Copyright (COPYRIGHT 1) while all other code, excluding that code which is in the libxml directory, is governed by COPYRIGHT 2.

-- COPYRIGHT 1:

New BSD License

Copyright (c) 2011, Robin Zhong <fbzhong@gmail.com>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the Robin Zhong nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

-- COPYRIGHT 2:

Copyright (c) 2012, John Rom <web@johnrom.com>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of John Rom nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.




