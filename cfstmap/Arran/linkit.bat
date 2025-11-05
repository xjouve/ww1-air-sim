rem    Create a temporary list file with the first entry being
rem    the Final Bgl name and the rest being all the suitably
rem    named bgls created from the Layouts (Arran00-Arran63)

echo >link.txt arran.bgl
dir >>link.txt arran??.bgl /b

rem    Run sclink from the directory above passing it the name
rem    of the temporary list file

..\sclink link.txt

rem    Copy the final Bgl to a CFS scenery folder (you will
rem    need to edit this to point to your required path to
rem    a suitable CFS scenery folder

copy arran.bgl "c:\program files\microsoft games\combat flight simulator\scenery\all\scenery\arran.bgl"

