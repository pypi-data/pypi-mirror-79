"""
This is an example for the usage of this package
"""
import os
from os.path import dirname
from iniparser import Config

os.environ["CONFIG_EXAMPLE_SECTION_FOO"] = "Before the run"
os.environ["CONFIG_EXAMPLE_SECTION_EXCLUDED"] = "This is not set"

if __name__ == "__main__":
    # Create the config object with the mode set to either "all_allowed" or "all_forbidden"
    config = Config(mode="all_allowed")
    # Specify the location of your ini files and read the files
    config.scan(dirname(__file__), recursive=False).read()
    # This is how you access the ini content
    old = config.config_rendered
    print(old)
    # This is how you can access the available environment variables
    print(config.environment_variables)
    # If you need to change a value of your config at runtime, just overwrite the according
    # environment variable
    os.environ["CONFIG_DEFAULT_THIS_KEY"] = "gets changed"
    # You can see the changes here
    print(
        "Changes on the config field test:",
        old["config"]["default"]["this_key"],
        "vs.",
        config.get("this_key"),
        sep="\n\t",
    )

    # Now if we change the mode and read the file again, we cannot change the field from earlier
    # any longer
    config.mode = "all_forbidden"
    config.read()
    # The available ENV variables are now
    print(config.environment_variables)
    # You can see the changes here
    print(
        "Changes on the config field test:",
        old["config"]["default"]["this_key"],
        "vs.",
        config.get("this_key"),
        sep="\n\t",
    )
