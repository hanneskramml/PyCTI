rule NetDiscovery
{
    meta:
        feat1 = "System Network Configuration Discovery"

    strings:
        $s1 = /ipconfig/ nocase
        $s2 = /ifconfig/ nocase

    condition:
        any of them
}