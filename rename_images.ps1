# Renames content/images/*.jpg to slug form so the frontend can resolve
# /portraits/{slug}.jpg. Run from the project root:
#     .\rename_images.ps1
#
# Safe: skips anything already renamed, and reports what it could not match
# instead of guessing.

$dir = "C:\Users\Kartik\OneDrive\Desktop\Codex Vitae\content\images"

$map = @{
    # Ancient Philosophy
    "seneca.htm"                = "seneca.jpg"        # NOT AN IMAGE -- see notes below
    "Epictectus.jpg"            = "epictetus.jpg"
    "aristootle.jpg"            = "aristotle.jpg"
    "plato.jpg"                 = "plato.jpg"
    "Heraclitus.jpg"            = "heraclitus.jpg"
    "Confucius.jpg"             = "confucius.jpg"
    "Diogenes.jpg"              = "diogenes.jpg"
    "Boethius.jpg"              = "boethius.jpg"

    # Literature
    "Nietzsche.jpg"             = "nietzsche.jpg"
    "Dostoevsky.jpg"            = "dostoevsky.jpg"
    "Tolstoy.jpg"               = "tolstoy.jpg"
    "Camus.jpg"                 = "camus.jpg"
    "Kafka.jpg"                 = "kafka.jpg"
    "Hemingway.jpg"             = "hemingway.jpg"
    "Pessoa.jpg"                = "pessoa.jpg"
    "Borges.jpg"                = "borges.jpg"
    "Cormac McCarthy.jpg"       = "cormac-mccarthy.jpg"
    "James Baldwin.jpg"         = "james-baldwin.jpg"
    "Virginia Woolf.jpg"        = "virginia-woolf.jpg"
    "Rilke.jpg"                 = "rilke.jpg"

    # Warrior
    "Miyamoto Musashi.jpg"      = "musashi.jpg"
    "Sun Tzu.jpg"               = "sun-tzu.jpg"
    "Bruce Lee.jpg"             = "bruce-lee.jpg"
    "Muhammad Ali.jpg"          = "muhammad-ali.jpg"
    "Kobe Bryant.jpg"           = "kobe-bryant.jpg"
    "Michael Jordan.jpg"        = "michael-jordan.jpg"
    "Khabib Nurmagomedov.jpg"   = "khabib.jpg"
    "Tyson Fury.jpg"            = "tyson-fury.jpg"
    "Roger Federer.jpg"         = "roger-federer.jpg"

    # Modern Thinkers
    "Carl Jung.jpg"             = "carl-jung.jpg"
    "Viktor Frankl.jpg"         = "viktor-frankl.jpg"
    "Rumi.jpg"                  = "rumi.jpg"
    "Alan Watts.jpg"            = "alan-watts.jpg"
    "Krishnamurti.jpg"          = "krishnamurti.jpg"
    "Joseph Campbell.jpg"       = "joseph-campbell.jpg"
    "Simone Weil.jpg"           = "simone-weil.jpg"
    "Steve Jobs.jpg"            = "steve-jobs.jpg"
    "Chalie Munger.jpg"         = "charlie-munger.jpg"
    "Naval Ravikant.jpg"        = "naval-ravikant.jpg"
    "Ryan Holiday.jpg"          = "ryan-holiday.jpg"
    "Nassim Taleb.jpg"          = "nassim-taleb.jpg"
}

# Deliberately NOT mapped -- decide these yourself first:
#   Sao Tzu.jpg     -> ambiguous. "Sun Tzu.jpg" already exists separately, so
#                      this is most likely a misspelled LAO TZU. Confirm by
#                      opening it, then rename to lao-tzu.jpg by hand.
#   photo-1739323147107-bc748671f498.avif
#                   -> unidentified stock filename. Open it, identify who it
#                      is, rename to <slug>.jpg (and convert from .avif).
#   seneca.htm      -> an HTML file, not a photo. The mapping above will
#                      rename it but it will still be broken. Replace with a
#                      real .jpg.
#
# Missing entirely (no file at all):
#   marcus-aurelius.jpg   <- most urgent; his figure JSON is already complete
#   mcgregor.jpg

Push-Location $dir
$renamed = 0
$skipped = 0

foreach ($old in $map.Keys) {
    $new = $map[$old]
    if ($old -eq $new) { continue }
    if (-not (Test-Path $old)) {
        Write-Host "SKIP (not found): $old" -ForegroundColor DarkGray
        $skipped++
        continue
    }
    if (Test-Path $new) {
        Write-Host "SKIP (target exists): $new" -ForegroundColor DarkGray
        $skipped++
        continue
    }
    Rename-Item -LiteralPath $old -NewName $new
    Write-Host "$old  ->  $new" -ForegroundColor Green
    $renamed++
}

Pop-Location
Write-Host ""
Write-Host "renamed: $renamed   skipped: $skipped" -ForegroundColor Cyan
Write-Host "Remaining files needing manual attention:" -ForegroundColor Yellow
Get-ChildItem $dir | Where-Object { $_.Name -notmatch '^[a-z0-9-]+\.(jpg|png|webp)$' } | ForEach-Object { Write-Host "  $($_.Name)" }
