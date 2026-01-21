$root = Split-Path -Parent $PSScriptRoot
Get-ChildItem -Path $root -Filter *.html -File -Recurse | Where-Object { $_.FullName -notmatch '\\docs\\|\\images\\' } | ForEach-Object {
    $path = $_.FullName
    try {
        $data = Get-Content -Raw -Encoding UTF8 -ErrorAction Stop -Path $path
    } catch {
        try { $data = Get-Content -Raw -Encoding Default -Path $path } catch { Write-Output "ERROR reading $path"; return }
    }
    $lower = $data.ToLower()
    $startIndex = $lower.IndexOf('<!doctype')
    if ($startIndex -lt 0) { $startIndex = 0 }
    $endIndex = $lower.IndexOf('</html>')
    if ($endIndex -ge 0) { $endIndex = $endIndex + 7 } else { $endIndex = $data.Length }
    $new = $data.Substring($startIndex, $endIndex - $startIndex)
    $new = $new -replace "`0", ''
    $replacementChar = [char]0xFFFD
    $new = $new -replace [regex]::Escape($replacementChar), ''
    if ($new -ne $data) {
        Set-Content -Path $path -Value $new -Encoding UTF8
        Write-Output "Fixed: $path"
    } else {
        Write-Output "NoChange: $path"
    }
}
Write-Output "Done."