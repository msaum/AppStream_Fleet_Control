#!/usr/bin/env bash
# -------------------------------------------------------------------------------
#
# -------------------------------------------------------------------------------
#

PROGNAME="fleet_control"

######################
# exit_error()
function exit_error() {
    echo "** Falure: $1"
    exit 1
}
echo "* Begin packaging ${PROGNAME} for AWS Lambda."
# Validate the tools we need are installed.
ZIP=`which zip`  || exit_error "Can't find the \'zip\' utility"

if [ -f "${PROGNAME}.zip" ]; then
    echo "** Removing old zip file: ${PROGNAME}.zip"
    rm -f ${PROGNAME}.zip
fi

echo "** Creating zip file package: ${PROGNAME}.zip"
${ZIP} -q -u -r ${PROGNAME}.zip setup.cfg *.py *.ini || exit_error "Creating or updating zip file failed"

echo "* End packaging ${PROGNAME} for AWS Lambda."
