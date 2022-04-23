# fsound-normalizer
Normalizes a .fss file in the following style:

- converts all effect commands to lowercase
- makes sure the first line starts with "t"
- removes comments
- removes "None" at the end of a line
- removes ; and writes every value into its own line
- removes loop-commands and writes out every loop
- writes volume to every note so volume commands get removed

In other words, the only remaining things to deal with in a normalized .fss are:
- tempo commands
- Kick/Snare with their length
- Noise with length and volume
- Tone with length and volume

Every value will exist on its own line and will always have the additional
parameters available!
