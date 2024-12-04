#!/bin/bash

# Word of caution: changing this can break update module, be vigilant

check_arch_updates() {
    official_updates=0
    aur_updates=0
    flatpak_updates=0
    tooltip="" # Initialize tooltip variable

    # Get the number of official updates using 'checkupdates'
    official_updates=$(checkupdates 2>/dev/null | wc -l)

    # Get the number of AUR updates using 'yay'
    aur_updates=$(yay -Qum 2>/dev/null | wc -l)

    # Calculate total updates
    total_updates=$((official_updates + aur_updates + flatpak_updates))

    # Build the tooltip for official updates
    tooltip="󰣇 Official $official_updates\n󰮯 AUR $aur_updates"

    # Check if flatpak is installed
    if command -v flatpak &>/dev/null; then
        # Get the number of Flatpak updates if flatpak is installed
        flatpak_updates=$(flatpak remote-ls --updates | wc -l)

        # Append Flatpak updates to the tooltip
        tooltip="$tooltip\n Flatpak $flatpak_updates"

        # Recalculate total updates
        total_updates=$((official_updates + aur_updates + flatpak_updates))
    fi

    # Output the result as a JSON object
    echo "{\"total\":\"$total_updates\", \"tooltip\":\"$tooltip\"}"
}

check_ubuntu_updates() {
    official_updates=0
    flatpak_updates=0

    # Check if flatpak is installed and get Flatpak updates if it is
    if command -v flatpak &>/dev/null; then
        flatpak_updates=$(flatpak remote-ls --updates | wc -l)
        # Always show Flatpak updates in the tooltip, even if there are none
        tooltip="󰕈 Official $official_updates\n Flatpak $flatpak_updates"
    else
        # If flatpak is not installed, only show official updates
        tooltip="󰕈 Official $official_updates"
    fi

    # Get the number of official updates using 'apt-get'
    official_updates=$(apt-get -s -o Debug::NoLocking=true upgrade | grep -c ^Inst)

    # Calculate total updates
    total_updates=$((official_updates + flatpak_updates))

    # Output the result as a JSON object
    echo "{\"total\":\"$total_updates\", \"tooltip\":\"$tooltip\"}"
}

check_fedora_updates() {
    official_updates=0
    flatpak_updates=0

    # Get the number of official updates using 'dnf'
    official_updates=$(dnf check-update -q | grep -v '^Loaded plugins' | grep -v '^No match for' | wc -l)

    # Calculate total updates
    total_updates=$((official_updates + flatpak_updates))

    # Check if flatpak is installed and get Flatpak updates if it is
    if command -v flatpak &>/dev/null; then
        flatpak_updates=$(flatpak remote-ls --updates | wc -l)
        # Always show Flatpak updates in the tooltip, even if there are none
        tooltip="󰣛 Official $official_updates\n Flatpak $flatpak_updates"
    else
        # If flatpak is not installed, only show official updates
        tooltip="󰣛 Official $official_updates"
    fi

    # Output the result as a JSON object
    echo "{\"total\":\"$total_updates\", \"tooltip\":\"$tooltip\"}"
}

check_opensuse_updates() {
    official_updates=0
    flatpak_updates=0

    # Check if flatpak is installed and get Flatpak updates if it is
    if command -v flatpak &>/dev/null; then
        flatpak_updates=$(flatpak remote-ls --updates | wc -l)
    fi

    # Get the number of official updates using 'dnf'
    official_updates=$(zypper lu | wc -l)

    # Calculate total updates
    total_updates=$((official_updates + flatpak_updates))

    # Check if flatpak is installed and get Flatpak updates if it is
    if command -v flatpak &>/dev/null; then
        flatpak_updates=$(flatpak remote-ls --updates | wc -l)
        # Always show Flatpak updates in the tooltip, even if there are none
        tooltip=" Official $official_updates\n Flatpak $flatpak_updates"
    else
        # If flatpak is not installed, only show official updates
        tooltip=" Official $official_updates"
    fi

    # Output the result as a JSON object
    echo "{\"total\":\"$total_updates\", \"tooltip\":\"$tooltip\"}"
}

case "$1" in
-arch)
    check_arch_updates
    ;;
-ubuntu)
    check_ubuntu_updates
    ;;
-fedora)
    check_fedora_updates
    ;;
-suse)
    check_opensuse_updates
    ;;
*)
    echo "0"
    ;;
esac
