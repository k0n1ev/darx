#!/usr/bin/env python3
# GUI for the Python scripts of DARx automation. Made on https://github.com/chriskiehl/Gooey
# Required Python 3

from gooey import Gooey, GooeyParser
import sys
import module_run
import module_home
import module_rvol
import module_calibrate
import config
import streamtologger
import json

def get_positions(): #getting positions of syringe pumps from config_[name of the host].ini
	return config.readvalue('antibody'), config.readvalue('reagent'), config.readvalue('needle')
antibody,reagent,needle= get_positions()

@Gooey(program_name="DarX Run", progress_regex=r".*?Cycle: (\d+)/(\d+)$", show_success_modal=False,optional_cols=3, progress_expr="x[0] / x[1] * 100", show_sidebar=True, program_description="Script configurator",image_dir="/home/pi/darx/icons/")
def parse_args():

	parser = GooeyParser()
	subparsers = parser.add_subparsers(help='options', dest='subparser_name')
	home_parser = subparsers.add_parser('Home')
	rvol_parser = subparsers.add_parser('Rvol')
	prerun_parser = subparsers.add_parser('Pre-run')
	run_parser = subparsers.add_parser('Run')
	manual_parser = subparsers.add_parser('Manual')
	release_parser = subparsers.add_parser('Release')

	home_fields = home_parser.add_argument_group('Homing all syringes', 'Current positions of syringes:\nAntibody: {} steps\nReagent: {} steps\nNeedle position: {}\n'.format(antibody,reagent,needle))
	rvol_fields = rvol_parser.add_argument_group('Measuring reactor volume', 'The routine permits to measure the reactor volume\nPress Start to execute',gooey_options={'columns': 3})
	prerun_fields = prerun_parser.add_argument_group('Pre-run homogenisation routines', 'Executes two in-out cycles to homogenise\nPlease provide the reactor volume in uL')
	run_fields = run_parser.add_argument_group('DarX parameters')
	manual_fields = manual_parser.add_argument_group('Control induvidial components', 'Press Start to execute', gooey_options={'columns': 3})
	release_fields = release_parser.add_argument_group('Release routines', 'Press Start to execute', gooey_options={'columns': 3})

	home_fields.add_argument("-home", metavar= "Homing utility", default='Press Start to execute')
	rvol_fields.add_argument("-rvol_speed", metavar= "Speed in, ml/min", default=0.5)
	prerun_fields.add_argument("-volout", metavar="Pre-run parameters", help='Execute pre-run routines. Indicate the reactor volume',default=5000, gooey_options={'validator':{'test': '0 < int(user_input) <= 10000','message': 'Must be between 1 and 10000 uL'
                        }}, type=int)
	prerun_fields.add_argument("-volout_uv", metavar="UV", default=False, action="store_true")

	run_fields_optional = run_parser.add_argument_group('Advanced parameters', gooey_options={'columns': 3})
	run_fields.add_argument("name", metavar="Experiment name", type=str)
	run_fields.add_argument("-onlygenerate", metavar="Generate only", default=False, action="store_true", help="Only generate .py file")
	run_fields.add_argument("-rvol", metavar="Reactor volume, uL", default=5000, gooey_options={'validator':{'test': '0 < int(user_input) <= 10000',
				'message': 'Must be between 1 and 10000 uL'
			}}, type=int)
	run_fields.add_argument("-cycles", metavar="Number of cycles", default=20, gooey_options={'validator':{'test': '0 < int(user_input) <= 200',
				'message': 'Must be between 1 and 200 cycles'
			}}, type=int)
	run_fields.add_argument("-add", metavar="Reagent volume, uL", default=50, gooey_options={'validator':{'test': '0 < int(user_input) <= 100',
				'message': 'Must be between 0 and 100 uL'
			}}, type=float)
	run_fields.add_argument("-coeff", metavar="Reagent decrease coefficient", default=0.95, gooey_options={'validator':{'test': '0 < float(user_input) <= 1',
				'message': 'Must be between 0 and 1'
			}}, type=float)
	run_fields_optional.add_argument("-time", metavar="Incubation time, sec", default=900, gooey_options={'validator':{'test': '0 <= int(user_input)',
				'message': 'Must be a positive number'
			}}, type=int)
	run_fields_optional.add_argument ("-speed_in", metavar="Speed in, mL/min", default=0.5, gooey_options={'validator':{'test': '0.05 <= float(user_input) <= 1',
				'message': 'Must be between 0.05 and 1 ml/min'
			}}, type=float)
	run_fields_optional.add_argument ("-speed_out", metavar="Speed out, mL/min", default=1, gooey_options={'validator':{'test': '0.05 <= float(user_input) <= 1',
				'message': 'Must be between 0.05 and 1 ml/min'
			}}, type=float)
	run_fields_optional.add_argument ("-speed_reagent", metavar="Speed reagent, mL/min", default=1, gooey_options={'validator':{'test': '0.05 <= float(user_input) <= 5',
				'message': 'Must be between 0.05 and 1 ml/min'
			}}, type=float)
	run_fields_optional.add_argument ("-uv_time", metavar="Time of UV measurement, sec", default=2, gooey_options={'validator':{'test': '0 <= float(user_input) <= 10',
				'message': 'Must be between 0 and 10 sec'
			}}, type=float)
	run_fields_optional.add_argument ("-mixing_time", metavar="Time of mixing between in/out, sec", default=30, gooey_options={'validator':{'test': '0 <= float(user_input) <= 300',
				'message': 'Must be between 0 and 300 sec'
			}}, type=float)

	manual_fields.add_argument("-reac", metavar="Reactor syringe, uL", default=0, gooey_options={'validator':{'test': '0 <= int(user_input) <= 10000',
				'message': 'Must be between 0 and 10000 uL'
			}}, type=float)
	manual_fields.add_argument ("-reac_speed", metavar="Speed reactor syringe, mL/min", default=0.5, gooey_options={'validator':{'test': '0.05 <= float(user_input) <= 5',
				'message': 'Must be between 0.05 and 5 ml/min'
			}}, type=float)
	manual_fields.add_argument("-reac_dir", metavar="Direction (reactor)",choices=['in','out'],default='in')

	manual_fields.add_argument("-reag", metavar="Reagent syringe, uL", default=0, gooey_options={'validator':{'test': '0 <= int(user_input) <= 1000',
				'message': 'Must be between 0 and 1000 uL'
			}}, type=float)
	manual_fields.add_argument ("-reag_speed", metavar="Speed reagent syringe, mL/min", default=0.5, gooey_options={'validator':{'test': '0.05 <= float(user_input) <= 5',
				'message': 'Must be between 0.05 and 5 ml/min'
			}}, type=float)
	manual_fields.add_argument("-reag_dir", metavar="Direction (reagent)",choices=['in','out'],default='in')
	manual_fields.add_argument ("-manual_mixing", metavar="Mixing time, sec", default=0, gooey_options={'validator':{'test': '0 <= float(user_input) <= 6000',
				'message': 'Must be between 0 and 6000 sec'
			}}, type=float)
	manual_fields.add_argument("-manual_needle", metavar="Move needle",choices=['up','down'])
	manual_fields.add_argument("-manual_uv", metavar="UV", default=False, action="store_true")

	cal_parser = subparsers.add_parser('UV')
	cal_fields = cal_parser.add_argument_group('UV Detector Calibration', 'Indicate standard concentrations below (BSA, mg/ml)\nIf no concentration provided, standard will be used', gooey_options={'columns': 6})
	for i in range (6):
		cal_fields.add_argument ("-conc_{}".format(i+1), metavar="#{}".format(i+1), type=str)

	release_fields.add_argument("name", metavar="Experiment name", type=str)
	release_fields.add_argument("-rvol", metavar="Reactor volume, uL", default=5000, gooey_options={'validator':{'test': '0 < int(user_input) <= 10000',
				'message': 'Must be between 1 and 10000 uL'
			}}, type=int)
	release_fields.add_argument("-time", metavar="Time of the release, min", default=300, gooey_options={'validator':{'test': '0 < int(user_input) <= 10000',
				'message': 'Must be between 1 and 10000 minutes'
			}}, type=int)
	release_fields.add_argument ("-speed_in", metavar="Speed in, mL/min", default=0.1, gooey_options={'validator':{'test': '0.05 <= float(user_input) <= 1',
				'message': 'Must be between 0.05 and 1 ml/min'
			}}, type=float)
	release_fields.add_argument ("-speed_out", metavar="Speed out, mL/min", default=0.1, gooey_options={'validator':{'test': '0.05 <= float(user_input) <= 1',
				'message': 'Must be between 0.05 and 1 ml/min'
			}}, type=float)
	release_fields.add_argument("-uv", metavar="UV", default=False, action="store_true")


	args = parser.parse_args()
	return args


if __name__ == '__main__':

	conf = parse_args()
	if conf.subparser_name == 'Run':
		module_run.run(conf)
	elif conf.subparser_name == 'Home':
		antibody,reagent,needle=get_positions()
		module_home.positions(antibody,reagent,needle)
		module_home.home(conf)
	elif conf.subparser_name == 'Rvol':
		module_rvol.volume(conf)
	elif conf.subparser_name == 'Manual':
		antibody,reagent,needle=get_positions()
		module_run.manual(conf,antibody,reagent,needle)
	elif conf.subparser_name == 'UV':
		module_calibrate.cal(conf)
	elif conf.subparser_name == 'Pre-run':
		module_run.prerun(conf)
	elif conf.subparser_name == 'Release':
		antibody,reagent,needle=get_positions()
		module_run.release(conf,antibody,reagent,needle)
