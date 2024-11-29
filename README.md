This is a Python project that helps fencers and coaches to record details analysis for a fencing bout.

When the program is run, it requires three arguments:

1. Name of the fencer on the left;
2. Name of the fencer on the right;
3. Weapon used;

Then it enters a loop where the interaction follows this pattern:

1. Produce a yaml file based on the `schema.yaml` file;
2. Enter to start a bout, i.e. when allez is called;
3. Enter again when a point is scored to start voice recording.  Note that this is not when a halt is called etc.
4. Print out the information that's available on in the schema.yaml file in a menu format;
5. Press Enter again to finish the recording; 
6. Parse the audio file to OpenAI after it's been transcribed.
7. Then pass it along with the yaml file and a prompt to Anthropic
8. Print out the result from Anthropic and append a new line to the yaml file.
