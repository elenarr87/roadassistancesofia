$root = Split-Path -Parent $PSScriptRoot
$results = @()
Get-ChildItem -Path $root -Filter *.html -File -Recurse | Where-Object { $_.FullName -notmatch '\\docs\\|\\images\\' } | ForEach-Object {
    $path = $_.FullName
    try { $content = Get-Content -Raw -Encoding UTF8 -Path $path } catch { $content = Get-Content -Raw -Encoding Default -Path $path }
    $titleMatch = [regex]::Match($content, '(?is)<title[^>]*>(.*?)</title>')
    $linkPattern = '(?is)<link\b[^>]*>'
    $hrefPattern = 'href\s*=\s*["'']([^"'']+)["'']'
    $relPattern = 'rel\s*=\s*["'']?canonical["'']?'
    $title = if ($titleMatch.Success) { $titleMatch.Groups[1].Value.Trim() } else { '' }
    $canon = ''
    $linkMatches = [regex]::Matches($content, $linkPattern)
    foreach ($lm in $linkMatches) {
        $tag = $lm.Value
        if ([regex]::IsMatch($tag, $relPattern, 'IgnoreCase')) {
            $hm = [regex]::Match($tag, $hrefPattern)
            if ($hm.Success) { $canon = $hm.Groups[1].Value.Trim(); break }
        }
    }
    $results += [pscustomobject]@{ Path=$path; Title=$title; Canonical=$canon }
}

Write-Output "Collected metadata from $($results.Count) files.`n"
# Find duplicate titles
$tGroups = $results | Group-Object -Property Title | Where-Object { $_.Count -gt 1 -and $_.Name -ne '' }
if ($tGroups.Count -eq 0) { Write-Output "No duplicate non-empty titles found." } else {
    Write-Output "Duplicate Titles:"; $tGroups | ForEach-Object { Write-Output "Title: '$($_.Name)'"; $_.Group | ForEach-Object { Write-Output " - $($_.Path)" } }
}

# Find duplicate canonicals
$cGroups = $results | Group-Object -Property Canonical | Where-Object { $_.Count -gt 1 -and $_.Name -ne '' }
if ($cGroups.Count -eq 0) { Write-Output "No duplicate canonicals found." } else {
    Write-Output "Duplicate Canonicals:"; $cGroups | ForEach-Object { Write-Output "Canonical: '$($_.Name)'"; $_.Group | ForEach-Object { Write-Output " - $($_.Path)" } }
}

# List files with missing titles or canonical
$missingTitle = $results | Where-Object { $_.Title -eq '' }
$missingCanon = $results | Where-Object { $_.Canonical -eq '' }
Write-Output "`nFiles missing title: $($missingTitle.Count)"
$missingTitle | ForEach-Object { Write-Output " - $($_.Path)" }
Write-Output "`nFiles missing canonical: $($missingCanon.Count)"
$missingCanon | ForEach-Object { Write-Output " - $($_.Path)" }
Write-Output "`nCheck complete."