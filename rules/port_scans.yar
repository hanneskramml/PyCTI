rule PortScan : APT1 APT28
{
    meta:
        feat1 = "Command-Line Interface"
        feat2 = "Source"

    strings:
        $s1 = /Scan/ nocase
        $s2 = "SSH Scan" nocase

    condition:
        any of them
}