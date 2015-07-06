@ECHO OFF
REM - sis_runner.batch
REM -
REM - This file can be used to schedule SIS exports to the Canvas LMS.
REM - Please see https://github.com/instructure/canvas-contrib for
REM - more information.
REM -


REM - Please set your API Token, export directory, account ID,
REM - Canvas URL, username, and password:

SETLOCAL

SET TOKEN=
SET ACCOUNT=
SET CANVAS_URL=https://canvas.instructure.com
SET EXPORT_DIRECTORY=C:\canvas-sis


SET CURL=C:\cURL\curl.exe

IF NOT DEFINED TOKEN (
	@ECHO Configuration incomplete! Exiting...
	GOTO:EOF
)

REM - Look for the zip file we'll upload
REM - This will send the first ZIP it finds
FOR /f "delims=" %%a IN ('DIR /B %EXPORT_DIRECTORY%\*.zip') DO @SET ZIP_FILE=%EXPORT_DIRECTORY%\%%a 
IF NOT DEFINED ZIP_FILE (
    @ECHO Unable to find a zip file in %EXPORT_DIRECTORY%! Exiting...
    GOTO:EOF
)

SET URL=%CANVAS_URL%/api/v1/accounts/%ACCOUNT%/sis_imports.json?
%CURL% -H "Content-Type: application/zip" -H "Authorization: Bearer %TOKEN%" --data-binary @%ZIP_FILE% %URL%^&import_type=instructure_csv
DEL %ZIP_FILE%
REM - Rather than delete, it would be better to move the file elsewhere

ENDLOCAL
