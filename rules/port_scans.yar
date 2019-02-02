rule PortScan : APT1 APT28
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