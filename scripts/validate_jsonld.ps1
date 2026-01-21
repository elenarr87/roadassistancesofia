$root = Split-Path -Parent $PSScriptRoot
Get-ChildItem -Path $root -Filter *.html -File -Recurse | Where-Object { $_.FullName -notmatch '\\docs\\|\\images\\' } | ForEach-Object {
    $path = $_.FullName
    try { $content = Get-Content -Raw -Encoding UTF8 -Path $path } catch { $content = Get-Content -Raw -Encoding Default -Path $path }
    $pattern = '(?s)<script[^>]*type=["'']application/ld\+json["''][^>]*>(.*?)</script>'
    $matches = [regex]::Matches($content, $pattern, 'IgnoreCase')
    if ($matches.Count -eq 0) { Write-Output "No JSON-LD: $path"; continue }
    $i=1
    foreach ($m in $matches) {
        $json = $m.Groups[1].Value.Trim()
        try {
            $null = $json | ConvertFrom-Json -ErrorAction Stop
            Write-Output "OK: $path (script#$i)"
        } catch {
            Write-Output "ERROR: $path (script#$i) -> $($_.Exception.Message)"
        }
        $i++
    }
}
Write-Output "Validation complete."