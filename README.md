Radikor
=============
Radikor is a python-based command-line Radiko player.

[Radiko](http://radiko.jp/) is an internet protocol silumcast radio service in Japan (only people in Japan can use this web service). Though you can listen Radiko through their web site, no APIs are provided for developpers. This application enables you to listen Radiko, and also record stream to mp3 file. 

This application is inspired by <https://gist.github.com/matchy2/3956266/>

## Requirement
dependent packages are rtmpdump/mplayer/ffmpeg/swftools. On Mac you can install these packages via brew.

```
brew install rtmpdump mplayer ffmpeg swftools
```

## Installation
To install RadikoPlayer, simply clone this repository and execute radiko_player.py.

```
git clone git@github.com:smrmkt/radikor.git
cd radiko_player/src
# play Tokyo-FM
python radiko_player.py play FMT
```

## Usage
You can choose play or record it. To listen broadcast program, you should assign station ID. For example, channel ID of TOKYO-FM is 'FMT.' Radio programs you can listen vary by region. All broadcast station list is [here](http://www.dcc-jpl.com/foltia/wiki/radikomemo). You can also get a list of available stations' names and ids.

#### Listen
To listen program, you should type:

```
python radikor.py play $CH_ID
```

#### Record
To record program, you should type:

```
python radikor.py record $CH_ID $DURATION $OUT_DIR
```

$DURATION is a record span (count by minutes). $OUT_DIR is a mp3 output output directory. File name is a $UNIX_TIMESTAMP.mp3 format. All options are required to execute this application.

#### List
To get station list, you should type:

```
python radikor.py list
```

You can get a station list like below:

```
Your region code is "JP14", and stations in your region are:
{
    "BAYFM78": "bayfm78", 
    "FMJ": "J-WAVE", 
    "FMT": "TOKYO FM", 
    "HOUSOU-DAIGAKU": "放送大学", 
    "INT": "InterFM", 
    "JORF": "ラジオ日本", 
    "LFR": "ニッポン放送", 
    "NACK5": "NACK5", 
    "QRR": "文化放送", 
    "RN1": "ラジオNIKKEI第1 ", 
    "RN2": "ラジオNIKKEI第2", 
    "TBS": "TBSラジオ", 
    "YFM": "ＦＭヨコハマ"
}
```

## Licence
Modified BSD License