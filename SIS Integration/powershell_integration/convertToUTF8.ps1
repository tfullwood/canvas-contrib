foreach($i in ls -name "C:\Users\kevinh\Desktop\courses1_csv\*.csv")
{
    $file = get-content "C:\Users\kevinh\Desktop\courses1_csv\$i"
    $encoding = New-Object System.Text.UTF8Encoding($False)
    [System.IO.File]::WriteAllLines("C:\Users\kevinh\Desktop\courses2_csv\" + $i, $file, $encoding)
}