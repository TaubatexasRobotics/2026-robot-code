param(
    [ValidateSet("enable","disable")]
    [string]$action
)

netsh interface set interface "Wi-Fi" $action