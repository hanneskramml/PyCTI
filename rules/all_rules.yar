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

rule CommandLineInterface : APT1 APT28
{
    meta:
        feat1 = "Command-Line Interface"

    strings:
        $s1 = /Scan/ nocase
        $s2 = "SSH Scan" nocase
        $s3 = /cmd.exe/ nocase
        $s4 = /rundll32.exe/ nocase

    condition:
        any of them
}

rule CredentialDumping : TURLA APT1 APT28
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

rule DataCompressed : APT1 APT28
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

rule DataFromLocalSystem : APT1 APT28
{
    meta:
        feat1 = "Data from Local System"

    strings:
        $s1 = /copy/ nocase
        $s2 = /xcopy/ nocase

    condition:
        any of them
}

rule EmailCollection : APT1 APT28
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

rule Scripting : APT1 APT28 APT29
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

rule SystemNetworkConfigurationDiscovery : TURLA
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



rule SpearphishingLink : TURLA APT1 APT28 APT29
{
    meta:
        feat1 = "Spearphishing Link"

    strings:
        $s1 = "Malicious Program" nocase

    condition:
        any of them
}

rule UserExecution : TURLA APT28 APT29
{
    meta:
        feat1 = "User Execution"

    strings:
        $s1 = "Installed by User" nocase

    condition:
        any of them
}

rule PowerShell : TURLA APT28 APT29
{
    meta:
        feat1 = "Power Shell"

    strings:
        $s1 = /.ps1/ nocase
        $s2 = "PowerShell" nocase

    condition:
        any of them
}

rule ProcessDiscovery : TURLA APT28
{
    meta:
        feat1 = "Process Discovery"

    strings:
        $s1 = "tasklist" nocase

    condition:
        any of them
}
