# Author: Nicolas Legrand <nicolas.legrand@cfin.au.dk>

import numpy as np
import time
import socket
import serial
from serial.tools import list_ports
from struct import unpack
from systole.detection import oxi_peaks
from systole.plotting import plot_oximeter, plot_events, plot_hr


class Oximeter():
    """Recording PPG signal with Nonin pulse oximeter.

    Parameters
    ----------
    serial : pySerial object
        The `serial` instance interfacing with the USB port.
    sfreq : int
        The sampling frequency of the recording. Defautl is 75 Hz.
    add_channels : int
        If int, will create as many additionnal channels. If None, no
        additional channels created.

    Attributes
    ----------
    instant_rr : list
        Time serie of instantaneous heartrate.
    n_channels : int | None
        Number of additional channels.
    recording : list
        Time serie of PPG signal.
    sfreq : int
        Sampling frequnecy. Default value is 75 Hz.
    threshold : list
        The threshold used to detect beat peaks. Will use the average +
        standars deviation.
    times : list
        Time vector (in seconds).
    diff : list
        Records the differential of the PPG signal. Used to detect heartbeat
        peaks.
    peaks : list
        List of 0 and 1. 1 index detected peaks.
    channels : list | dict
        Additional channels to record. Will continuously record *n_channels*
        additional channels in parallel of `recording` with default `0` as
        defalut value.
    serial : PySerial instance
        PySerial object indexing the USB port to read.
    rr : list or None
        RR intervals time course. The time course will be generated if
        :py:func:`self.find_peaks` is used.

    Examples
    --------
    First, you will need to define a :py:func:`serial` instance, indexing the
    USB port where the Nonin Pulse Oximeter is plugged.

    >>> import serial
    >>> ser = serial.Serial('COM4')

    This instance is then used to create an :py:func:`Oximeter` instance that
    will be used for the recording.

    >>> from ecg.recording import Oximeter
    >>> oximeter = Oximeter(serial=ser, sfreq=75)

    Use the :py:func:`setup` method to initialize the recording. This will find
    the start byte to ensure that all the forthcoming data is in Synch. You
    should not wait more than ~10s between the setup and the recording,
    otherwise the buffer will start to overwrite the data.

    >>> oximeter.setup()

    Two methods are availlable to record PPG signal:

    1. The :py:func:`read` function.

    Will continuously record for certain amount of time (specified by the
    *duration* parameter, in seconds). This is the easiest and most robust
    method, but it is not possible to run instructions in the meantime.

    >>> oximeter.read(duration=10)

    2. The :py:func:`readInWaiting` function.

    Will read all the availlable bytes (up to 10 seconds of recording). When
    inserted into a while loop, it allows to record PPG signal together with
    other scripts.

    >>> import time
    >>> tstart = time.time()
    >>> while time.time() - tstart < 10:
    >>>     oximeter.readInWaiting()
    >>>     # Insert code here

    The recorded signal can latter be inspected using the :py:func:`plot()`
    method.

    >>> oximeter.plot()

    .. warning:: Data read from the serial port are appended to list and
      processed for pulse detection and instantaneous heart rate estimation.
      The time required to append new data to the recording will increase as
      its size increase. You should beware that this processing time does not
      exceed the sampling frequency (i.e. 75Hz or 0.013 seconds per sample for
      Nonin pulse oximeters) to allow continuous recording and fast processing
      of in waiting samples. We recommend storing regularly 5 minutes recording
      as .npy file using the :py:func:save() function.
    """
    def __init__(self, serial, sfreq=75, add_channels=None):

        self.serial = serial
        self.lag = 0
        self.sfreq = sfreq
        self.dist = int(self.sfreq * 0.2)

        # Initialize recording with empty lists
        self.instant_rr = []
        self.recording = []
        self.times = []
        self.n_channels = add_channels
        self.threshold = []
        self.diff = []
        self.peaks = []
        if add_channels is not None:
            self.channels = {}
            for i in range(add_channels):
                self.channels['Channel_' + str(i)] = []
        else:
            self.channels = None

    def add_paquet(self, paquet, window=1):
        """Read a portion of data.

        Parameters
        ----------
        paquet : int
            The data to record. Should be an integer between 0 and 240.
        window : int or float
            Length of the window used to compute threshold (seconds). Default
            is `1`.

        Returns
        -------
        Oximeter instance.

        Notes
        -----
        Will automatically calculate the differential, threshold and increment
        additional channles with 0 if provided.
        """

        # Store new data
        self.recording.append(paquet)
        self.peaks.append(0)

        # Add 0 to the additional channels
        if self.channels is not None:
            for ch in self.channels:
                self.channels[ch].append(0)

        # Update times vector
        if not self.times:
            self.times = [0]
        else:
            self.times.append(len(self.times)/self.sfreq)

        # Update threshold
        window = int(window * self.sfreq)
        self.threshold.append((np.mean(self.recording[-window:]) +
                               np.std(self.recording[-window:])))

        # Store new differential if not exist
        if not self.diff:
            self.diff = [0]
        else:
            self.diff.append(self.recording[-1] - self.recording[-2])

            # Is it a threshold crossing value?
            if paquet > self.threshold[-1]:

                # Is the new differential zero or crossing zero?
                if (self.diff[-1] <= 0) & (self.diff[-2] > 0):

                    # Is it far enough from the previous peak (0.2 s)?
                    if not any(self.peaks[-15:]):
                        self.peaks[-1] = 1

        # Update instantaneous heart rate
        if sum(self.peaks) >= 2:
            self.instant_rr.append(
                (np.diff(np.where(self.peaks)[0])[-1]/self.sfreq)*1000)
        else:
            self.instant_rr.append(float('nan'))

        return self

    def check(self, paquet):
        """Check if the provided paquet is correct

        Parameters
        ----------
        paquet : list
            The paquet to inspect.
        """
        check = False
        if len(paquet) >= 5:
            if paquet[0] == 1:
                if (paquet[1] >= 0) & (paquet[1] <= 255):
                    if (paquet[2] >= 0) & (paquet[2] <= 255):
                        if paquet[3] <= 127:
                            if paquet[4] == sum(paquet[:4]) % 256:
                                check = True

        return check

    def find_peaks(self, **kwargs):
        """Find peaks in recorded signal.

        Returns
        -------
        Oximeter instance. The peaks occurences are stored in the `peaks`
        attribute.

        Other Parameters
        ----------------
        **kwargs : `~systole.detection.oxi_peaks` properties.
        """
        # Peak detection
        resampled_signal, peaks = oxi_peaks(self.recording,
                                            new_sfreq=75, **kwargs)

        # R-R intervals (in miliseconds)
        self.rr = (np.diff(np.where(peaks)[0])/self.sfreq) * 1000

        # Beats per minutes
        self.bpm = 60000/self.rr

        return self

    def plot_events(self, ax=None):
        """Visualize the distribution of events stored in additional channels.

        Returns
        -------
        fig, ax : Matplotlib instances.
            The figure and axe instances.
        """
        ax = plot_events(self, ax=ax)

        return ax

    def plot_hr(self, ax=None):
        """Plot heartrate extracted from PPG recording.

        Returns
        -------
        fig, ax : Matplotlib instances.
            The figure and axe instances.
        """
        ax = plot_hr(self, ax=ax)

        return ax

    def plot_recording(self, ax=None):
        """Plot recorded signal.

        Returns
        -------
        fig, ax : Matplotlib instances.
            The figure and axe instances.
        """
        ax = plot_oximeter(self, ax=ax)

        return ax

    def read(self, duration):
        """Read PPG signal for some amount of time.

        Parameters
        ----------
        duration : int or float
            Length of the desired recording time.
        """
        tstart = time.time()
        while time.time() - tstart < duration:
            if self.serial.inWaiting() >= 5:
                # Store Oxi level
                paquet = list(self.serial.read(5))
                if self.check(paquet):
                    self.add_paquet(paquet[2])
                else:
                    self.setup()
        return self

    def readInWaiting(self, stop=False):
        """Read in wainting oxi data.

        Parameters
        ----------
        stop : bool
            Stop the recording when an error is detected. Default is *False*.
        """
        # Read oxi
        while self.serial.inWaiting() >= 5:
            # Store Oxi level
            paquet = list(self.serial.read(5))
            if self.check(paquet):
                self.add_paquet(paquet[2])
            else:
                if stop is True:
                    raise ValueError('Synch error')
                else:
                    print('Synch error')
                    while True:
                        self.serial.reset_input_buffer()
                        paquet = list(self.serial.read(5))
                        if self.check(paquet=paquet):
                            break

    def save(self, fname):
        """Save the recording instance.

        Parameters
        ----------
        fname : str
            The file name.
        """
        if len(self.peaks) != len(self.recording):
            self.peak = np.zeros(len(self.recording))

        if len(self.instant_rr) != len(self.recording):
            self.instant_rr = np.zeros(len(self.recording))

        if len(self.times) != len(self.recording):
            self.times = np.zeros(len(self.recording))

        if len(self.threshold) != len(self.recording):
            self.threshold = np.zeros(len(self.recording))

        recording = np.array([np.asarray(self.recording),
                              np.asarray(self.peaks),
                              np.asarray(self.instant_rr),
                              np.asarray(self.times),
                              np.asarray(self.threshold)])

        np.save(fname, recording)

    def setup(self, read_duration=1, clear_peaks=True):
        """Find start byte and read a portion of signal.

        Parameters
        ----------
        read_duration : int
            Length of signal to record after setup. Default is set to 1 second.
        clear_peaks : bool
            If *True*, will remove detected peaks.

        Notes
        -----
        .. warning:: setup() clear the input buffer and will remove previously
        recorded data from the Oximeter instance. Peaks detected during this
        procedure are automatically removed.
        """
        # Reset recording instance
        self.__init__(serial=self.serial, add_channels=self.n_channels)
        while True:
            self.serial.reset_input_buffer()
            paquet = list(self.serial.read(5))
            if self.check(paquet=paquet):
                break
        self.read(duration=read_duration)

        # Remove peaks
        if clear_peaks is True:
            self.peaks = [0] * len(self.peaks)

        return self

    def waitBeat(self):
        """Read Oximeter until a heartbeat is detected.
        """
        while True:
            if self.serial.inWaiting() >= 5:
                # Store Oxi level
                paquet = list(self.serial.read(5))
                if self.check(paquet):
                    self.add_paquet(paquet[2])
                    if any(self.peaks[-2:]):  # Peak found
                        break
                else:
                    print('Synch error')
        return self


class BrainVisionExG():
    """Recording ECG signal through TCPIP.

    Parameters
    ----------
    ip : str
        The IP address of the recording computer.
    sfreq : int
        The sampling frequency.
    port : int
        The port to listen. Default is 51244 (32 bits). Change port to 51234 to
        connect to 16Bit RDA-port

    Examples
    --------
    This instance is then used to create an :py:func:`BrainVisionExG` instance
    that will be used for the recording.

    >>> from ecg.recording import BrainVisionExG
    >>> exg = BrainVisionExG(ip='xxx.xxx.xx', sfreq=1000).read(30)

    Use the :py:func:`read` method to record some signal and save it in the
    `exg` dictionnary.

    .. warning:: The signals received fom the host are appened to a list. This
       process can require more time at each iteration as the signal length
       increase in memory. You should alway make sure that this will not
       interfer with other task and regularly save intermediate recording to
       save resources.

    Notes
    -----
    This class is adapted from the RDA client for python made available by
    Brain Products on the following link:
        https://www.brainproducts.com/downloads.php?kid=2
    """

    def __init__(self, ip, sfreq, port=51244):

        self.ip = ip
        self.port = port
        self.sfreq = sfreq
        self.dist = int(self.sfreq * 0.2)
        self.recording = []

        # Create a tcpip socket
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # block counter to check overflows of tcpip buffer
        self.lastBlock = -1

        # Connect to recorder host
        self.con.connect((self.ip, self.port))

        # Marker dict for storing marker information
        self.marker = {'position': 0, 'points': 0, 'channel': -1,
                       'type': "", 'description': ""}

    def RecvData(self, requestedSize):
        """Helper function for receiving whole message"""
        returnStream = b''
        while len(returnStream) < requestedSize:
            databytes = self.con.recv(requestedSize - len(returnStream))
            if not databytes:
                raise RuntimeError
            returnStream += databytes

        return returnStream

    def SplitString(self, raw):
        """Helper function for splitting a raw array of zero terminated
        strings (C) into an array of python strings"""

        raw = raw.decode()
        stringlist = []
        s = ""
        for i in range(len(raw)):
            if raw[i] != '\x00':
                s = s + raw[i]
            else:
                stringlist.append(s)
                s = ""
        return stringlist

    def GetProperties(self, rawdata):
        """Helper function for extracting ExG properties from a raw data array
        read from tcpip socket"""

        # Extract numerical data
        (channelCount, samplingInterval) = unpack('<Ld', rawdata[:12])

        # Extract resolutions
        resolutions = []
        for c in range(channelCount):
            index = 12 + c * 8
            restuple = unpack('<d', rawdata[index:index+8])
            resolutions.append(restuple[0])

        # Extract channel names
        channelNames = self.SplitString(rawdata[12 + 8 * channelCount:])

        return (channelCount, samplingInterval, resolutions, channelNames)

    def GetData(self, rawdata, channelCount):
        """Helper function for extracting eeg and marker data from a raw data
        array read from tcpip socket"""

        # Extract numerical data
        (block, points, markerCount) = unpack('<LLL', rawdata[:12])

        # Extract eeg data as array of floats
        data = []
        for i in range(points * channelCount):
            index = 12 + 4 * i
            value = unpack('<f', rawdata[index:index+4])
            data.append(value[0])

        # Extract markers
        markers = []
        index = 12 + 4 * points * channelCount
        for m in range(markerCount):
            markersize = unpack('<L', rawdata[index:index+4])

            ma = self.marker.copy()
            (ma['position'], ma['points'], ma['channel']) = \
                unpack('<LLl', rawdata[index+4:index+16])
            typedesc = self.SplitString(rawdata[index+16:index+markersize[0]])
            ma['type'] = typedesc[0]
            ma['description'] = typedesc[1]

            markers.append(ma)
            index = index + markersize[0]

        return (block, points, markerCount, data, markers)

    def read(self, duration):
        """Read incoming signals.

        Parameters
        ----------
        duration : float
            The length of the recording.

        Returns
        -------
        recording : dict
            Dictionnary with channel name as key.

        Notes
        -----
        Duration will be converted to expected signal length (duration * sfreq)
        to ensure consistent recording.
        """
        while True:

            # Get message header as raw array of chars
            rawhdr = self.RecvData(24)

            # Split array into usefull information id1 to id4 are constants
            (id1, id2, id3, id4, msgsize, msgtype) = unpack('<llllLL', rawhdr)

            # Get data part of message, which is of variable size
            rawdata = self.RecvData(msgsize - 24)

            # Perform action dependend on the message type
            if msgtype == 1:
                # Start message, extract eeg properties and display them
                (channelCount, samplingInterval, resolutions, channelNames) = \
                    self.GetProperties(rawdata)
                # reset block counter
                self.lastBlock = -1

                print("Reading TCP/IP connection (" +
                      str(channelCount) + " channels found). "
                      + str(resolutions) + " Hz. "
                      + str(samplingInterval) + " samples. "
                      + str(channelNames))

            elif msgtype == 4:
                # Data message, extract data and markers
                (block, points, markerCount, data, markers) = \
                    self.GetData(rawdata, channelCount)

                # Check for overflow
                if self.lastBlock != -1 and block > self.lastBlock + 1:
                    print("*** Overflow with " +
                          str(block - self.lastBlock) + " datablocks ***")
                self.lastBlock = block

                # Print markers, if there are some in actual block
                if markerCount > 0:
                    for m in range(markerCount):
                        print("Marker " + markers[m]['description'] +
                              " of type " + markers[m]['type'])

                # Put data at the end of actual buffer
                self.recording.extend(data)
                if ((len(self.recording)/self.sfreq)/channelCount) >= duration:
                    break
            elif msgtype == 3:
                # Stop message, terminate program
                print("Stop")

        recording = {}
        for ch_name, ch_nb in zip(channelNames, range(channelCount)):
            recording[ch_name] = np.array(self.recording[ch_nb::channelCount])

        return recording

    def close(self):
        """Close TCPIP connections"""
        self.con.close()


def findOximeter():
    """Find USB port where Nonin Pulse Oximeter is plugged.

    Returns
    -------
    port : str or None
        The port reference or None if no device found.

    Notes
    -----
    This function is only compatible with Windows 10.
    """
    port = None
    usbList = list(list_ports.comports())

    for usb in usbList:
        print('Connecting on device found in USB port ' + usb.device)

        try:
            Oximeter(serial=serial.Serial(usb.device)).setup().read(.2)
            port = usb.device
        except:
            print('Invalid signal.')

    return port
