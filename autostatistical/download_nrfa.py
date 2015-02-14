# -*- coding: utf-8 -*-

# OH Auto Statistical
# Copyright (C) 2015  Florenz A. P. Hollebrandse
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from floodestimation import db
from floodestimation import loaders


def main():

    print("Removing existing data.")
    db.reset_db_tables()

    print("Loading new data.")
    db_session = db.Session()
    loaders.nrfa_to_db(db_session, incl_pot=False)

    try:
        print("Saving new data.")
        db_session.commit()
        print("Data loaded successfully.")
    finally:
        db_session.close()


if __name__ == "__main__":
    main()
