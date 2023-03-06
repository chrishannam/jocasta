import click
import logging

from jocasta.config import load_config
from jocasta.inputs.serial_connector import ArduinoConfiguration

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


@click.command()
@click.option('--forever', '-f', default=False, is_flag=True)
@click.option('--config-file', '-c', required=False, type=click.Path(exists=True))
@click.option('--device', '-d', required=False, type=click.Path(exists=True))
def main(forever, config_file, device):
    logger = logging.getLogger(__name__)

    logger.info('Starting')
    if config_file:
        logger.info('Using %s configuration file', config_file)
        configuration = load_config(config_file)
        a = 1
    else:
        config = ArduinoConfiguration(device=device)
    logger.info('Done')
    #
    #
    # controller = Controller(config=configuration)
    #
    # if forever:
    #     while True:
    #         readings: Readings = controller.get_readings()
    #         controller.send_readings(readings=readings)
    #         a = 1


if __name__ == '__main__':
    main()
