rule SystemNetworkConfigurationDiscovery
{
    meta:
        feat1 = "System Network Configuration Discovery"

    strings:
        $s1 = /ipconfig/ nocase
        $s2 = /ifconfig/ nocase
        $s3 = /arp/ nocase
        $s4 = /nbtstat/ nocase
        $s5 = /net/ nocase
        $s6 = /route/ nocase

    condition:
        any of them
}

rule ConductActiveScanning
{
    meta:
        feat1 = "Conduct active scanning"

    strings:
        $s1 = /ipconfig/ nocase
        $s2 = /ifconfig/ nocase
        $s3 = /Scan/ nocase
        $s4 = "SSH Scan" nocase
        $s5 = /nmap/ nocase
        $s6 = /net start/ nocase
        $s7 = /route/ nocase

    condition:
        any of them
}

rule CredentialDumping
{
    meta:
        feat1 = "Credential Dumping"

    strings:
        $s1 = /pwdumpx.exe/ nocase
        $s2 = /secretsdump.py/ nocase
        $s3 = "Mimikatz" nocase
        $s4 = "gsecdump" nocase
        $s5 = "pwdump" nocase
        $s6 = "Cachedump" nocase
        $s7 = "Windows Credential Editor" nocase

    condition:
        any of them
}

rule DataCompressed
{
    meta:
        feat1 = "Data Compressed"

    strings:
        $s1 = /zip/ nocase
        $s2 = "WinRAR" nocase
        $s3 = /temp.zip/ nocase

    condition:
        any of them
}

rule DataFromLocalSystem
{
    meta:
        feat1 = "Data from Local System"

    strings:
        $s1 = /copy/ nocase
        $s2 = /xcopy/ nocase

    condition:
        any of them
}

rule EmailCollection
{
    meta:
        feat1 = "Email Collection"

    strings:
        $s1 = /.pst/ nocase
        $s2 = /.ost/ nocase
        $s3 = /findstr/ nocase
        $s4 = "MailSniper" nocase
        $s5 = "GETMAIL" nocase
        $s6 = "MAPIGET" nocase

    condition:
        any of them
}

rule Scripting
{
    meta:
        feat1 = "Scripting"

    strings:
        $s1 = /.bat/ nocase
        $s2 = /.cmd/ nocase
        $s3 = /.vbs/ nocase
        $s4 = /.ps1/ nocase
        $s5 = "cscript" nocase
        $s6 = "PowerShell" nocase

    condition:
        any of them
}

rule SpearphishingLink
{
    meta:
        feat1 = "Spearphishing Link"

    strings:
        $s1 = "Malicious Program" nocase

    condition:
        any of them
}

rule UserExecution
{
    meta:
        feat1 = "User Execution"

    strings:
        $s1 = "Installed by User" nocase

    condition:
        any of them
}

rule PowerShell
{
    meta:
        feat1 = "Power Shell"

    strings:
        $s1 = /.ps1/ nocase
        $s2 = "PowerShell" nocase

    condition:
        any of them
}

rule StandardApplicationLayerProtocol
{
    meta:
        feat1 = "Standard Application Layer Protocol"

    strings:
        $s1 = "HTTP" nocase
        $s2 = "HTTPS" nocase
        $s3 = "SMTP" nocase

    condition:
        any of them
}
