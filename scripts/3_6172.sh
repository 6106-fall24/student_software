#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
   sudo -E $0
else
   echo "Giving everyone access to kernel perf counters"
   if ! grep -q "kernel.perf_event_paranoid = 0" /etc/sysctl.conf; then
      echo "kernel.perf_event_paranoid = 0" >> /etc/sysctl.conf
   fi

   echo "Installing vs code live share dependencies"
   wget -O ~/vsls-reqs https://aka.ms/vsls-linux-prereq-script
   chmod +x ~/vsls-reqs
   ~/vsls-reqs
fi
