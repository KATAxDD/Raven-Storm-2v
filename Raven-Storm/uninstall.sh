#!/bin/bash

echo "[i] We will now uninstall Raven-Storm..."
echo "[i] This will delete all backups."
read -p "Are you sure you want to proceed? (y/N) " -r
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "[i] Uninstallation aborted."
    exit 1
fi

echo "[i] Deleting /usr/bin/rst..."
if sudo rm -i /usr/bin/rst; then
    echo "[i] /usr/bin/rst deleted."
else
    echo "[!] Failed to delete /usr/bin/rst. Exiting."
    exit 1
fi

echo "[i] Deleting /usr/share/Raven-Storm..."
if sudo rm -rf -i /usr/share/Raven-Storm; then
    echo "[i] /usr/share/Raven-Storm deleted."
else
    echo "[!] Failed to delete /usr/share/Raven-Storm. Exiting."
    exit 1
fi

echo "[i] Raven-Storm successfully uninstalled."
exit 0
