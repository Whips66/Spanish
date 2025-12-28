# PowerShell script to add subjunctive tenses to all verbs

# Read the JSON file
$json = Get-Content "verbs.json" -Raw -Encoding UTF8 | ConvertFrom-Json

# Subjunctive conjugation rules
function Get-SubjunctiveConjugations {
    param(
        [string]$infinitive,
        [hashtable]$presente,
        [hashtable]$preterito
    )
    
    $conjugations = @{
        "presente subjuntivo" = @{}
        "imperfecto subjuntivo" = @{}
    }
    
    # Presente de subjuntivo - based on yo form of presente
    # For irregular verbs, we need custom logic
    $irregularPresenteSubj = @{
        "ser" = @{"yo"="sea"; "tú"="seas"; "él/ella"="sea"; "nosotros"="seamos"; "vosotros"="seáis"; "ellos"="sean"}
        "estar" = @{"yo"="esté"; "tú"="estés"; "él/ella"="esté"; "nosotros"="estemos"; "vosotros"="estéis"; "ellos"="estén"}
        "haber" = @{"yo"="haya"; "tú"="hayas"; "él/ella"="haya"; "nosotros"="hayamos"; "vosotros"="hayáis"; "ellos"="hayan"}
        "ir" = @{"yo"="vaya"; "tú"="vayas"; "él/ella"="vaya"; "nosotros"="vayamos"; "vosotros"="vayáis"; "ellos"="vayan"}
        "saber" = @{"yo"="sepa"; "tú"="sepas"; "él/ella"="sepa"; "nosotros"="sepamos"; "vosotros"="sepáis"; "ellos"="sepan"}
        "dar" = @{"yo"="dé"; "tú"="des"; "él/ella"="dé"; "nosotros"="demos"; "vosotros"="deis"; "ellos"="den"}
        "ver" = @{"yo"="vea"; "tú"="veas"; "él/ella"="vea"; "nosotros"="veamos"; "vosotros"="veáis"; "ellos"="vean"}
    }
    
    if ($irregularPresenteSubj.ContainsKey($infinitive)) {
        $conjugations["presente subjuntivo"] = $irregularPresenteSubj[$infinitive]
    }
    else {
        # Get stem from yo form of presente
        $yoForm = $presente["yo"]
        $stem = ""
        
        # Remove -o ending from yo form for stem
        if ($yoForm -match "^(.+)o$") {
            $stem = $Matches[1]
        }
        elseif ($yoForm -match "^(.+)oy$") {  # for estar, dar
            $stem = $Matches[1] + "é"
        }
        else {
            # Irregular - try to handle
            $stem = $yoForm -replace "o$", ""
        }
        
        # Determine endings based on infinitive type
        if ($infinitive -match "ar$") {
            $conjugations["presente subjuntivo"] = @{
                "yo" = $stem + "e"
                "tú" = $stem + "es"
                "él/ella" = $stem + "e"
                "nosotros" = $stem + "emos"
                "vosotros" = $stem + "éis"
                "ellos" = $stem + "en"
            }
        }
        else {  # -er or -ir verbs
            $conjugations["presente subjuntivo"] = @{
                "yo" = $stem + "a"
                "tú" = $stem + "as"
                "él/ella" = $stem + "a"
                "nosotros" = $stem + "amos"
                "vosotros" = $stem + "áis"
                "ellos" = $stem + "an"
            }
        }
    }
    
    # Imperfecto de subjuntivo - based on ellos form of pretérito
    $ellosPreterito = $preterito["ellos"]
    if ($ellosPreterito -match "^(.+)ron$") {
        $stem = $Matches[1]
        $conjugations["imperfecto subjuntivo"] = @{
            "yo" = $stem + "ra"
            "tú" = $stem + "ras"
            "él/ella" = $stem + "ra"
            "nosotros" = $stem + "ramos"
            "vosotros" = $stem + "rais"
            "ellos" = $stem + "ran"
        }
    }
    
    return $conjugations
}

# Process each verb
foreach ($verbKey in $json.PSObject.Properties.Name) {
    $verb = $json.$verbKey
    
    Write-Host "Processing: $verbKey"
    
    # Convert hashtables for processing
    $presenteHash = @{}
    foreach ($prop in $verb.presente.PSObject.Properties) {
        $presenteHash[$prop.Name] = $prop.Value
    }
    
    $preteritoHash = @{}
    foreach ($prop in $verb.pretérito.PSObject.Properties) {
        $preteritoHash[$prop.Name] = $prop.Value
    }
    
    # Get subjunctive conjugations
    $subjunctive = Get-SubjunctiveConjugations -infinitive $verbKey -presente $presenteHash -preterito $preteritoHash
    
    # Add to verb object
    $verb | Add-Member -MemberType NoteProperty -Name "presente subjuntivo" -Value (ConvertTo-Json $subjunctive["presente subjuntivo"] -Compress | ConvertFrom-Json) -Force
    $verb | Add-Member -MemberType NoteProperty -Name "imperfecto subjuntivo" -Value (ConvertTo-Json $subjunctive["imperfecto subjuntivo"] -Compress | ConvertFrom-Json) -Force
}

# Write back to JSON file
$json | ConvertTo-Json -Depth 10 | Set-Content "verbs_with_subjunctive.json" -Encoding UTF8

Write-Host "`nDone! Created verbs_with_subjunctive.json"
Write-Host "Review the file and if it looks good, rename it to verbs.json"
