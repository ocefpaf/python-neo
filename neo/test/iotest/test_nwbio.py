#
"""
Tests of neo.io.nwbio
"""

from __future__ import unicode_literals, print_function, division, absolute_import
import unittest
from neo.io.nwbio import NWBIO
from neo.test.iotest.common_io_test import BaseTestIO
from neo.core import AnalogSignal, SpikeTrain, Event, Epoch, IrregularlySampledSignal, Segment, Unit, Block, ChannelIndex
import pynwb
from pynwb import *
import quantities as pq
import numpy as np

class TestNWBIO(unittest.TestCase, ):
    ioclass = NWBIO
    files_to_download =  [
        # My NWB files
              '/home/elodie/NWB_Files/NWB_File_python_3_pynwb_101_ephys_data_bis.nwb', # File created with the latest version of pynwb=1.0.1 only with ephys data File on my github page

        # Files from Allen Institute
        # NWB files downloadable from http://download.alleninstitute.org/informatics-archive/prerelease/
###              '/home/elodie/NWB_Files/NWB_org/H19.28.012.11.05-2.nwb'
#              '/home/elodie/NWB_Files/NWB_org/H19.28.012.11.05-3.nwb'
#              '/home/elodie/NWB_Files/NWB_org/H19.28.012.11.05-4.nwb'
###              '/home/elodie/NWB_Files/NWB_org/H19.29.141.11.21.01.nwb'
#              '/home/elodie/NWB_Files/NWB_org/behavior_ophys_session_775614751.nwb'
#              '/home/elodie/NWB_Files/NWB_org/ecephys_session_785402239.nwb'

        # File written with NWBIO class()
###              '/home/elodie/env_NWB_py3/my_notebook/my_first_test_neo_to_nwb.nwb'
###              '/home/elodie/env_NWB_py3/my_notebook/my_first_test_neo_to_nwb_test_NWBIO.nwb'
#              '/home/elodie/env_NWB_py3/my_notebook/my_first_test_neo_to_nwb_test_NWBIO_2.nwb'
###            '/home/elodie/env_NWB_py3/my_notebook/my_first_test_neo_to_nwb_test_NWBIO.nwb'
    ]
    entities_to_test = files_to_download


    def test_nwbio(self):
        # read the blocks
        reader = NWBIO(filename=self.files_to_download[0], mode='r')
        print("reader = ", reader)
#        print("reader.read() = ", reader.read())
        
        print("reader.read_block() = ", reader.read_block())
        print("   ")
#        blocks = reader.read(lazy=False)

        #-------------------------------------------------------
        blocks=[]
        for ind in range(2): # 2 blocks
            blk = Block(name='%s' %ind)
            blocks.append(blk)
        #-------------------------------------------------------

        # access to segments
        for block in blocks:
            # Tests of Block
            self.assertTrue(isinstance(block.name, str))
            # Segment
            for segment in block.segments:
                self.assertEqual(segment.block, block)
                # AnalogSignal
                for asig in segment.analogsignals:
                    self.assertTrue(isinstance(asig, AnalogSignal))
                    self.assertTrue(asig.sampling_rate, pq.Hz)
                    self.assertTrue(asig.units, pq)
                # Spiketrain
                for st in segment.spiketrains:
                    self.assertTrue(isinstance(st, SpikeTrain))          


    def test_segment(self, **kargs):
        seg = Segment(index=5)
        r = NWBIO(filename=self.files_to_download[0], mode='r')


#        #-------------------------------------------------------
#        blocks=[]
#        for ind in range(2): # 2 blocks
#            blk = Block(name='%s' %ind)
#            blocks.append(blk)
#        #-------------------------------------------------------
#        seg_nwb = r.read()
##        seg_nwb = r.read(blocks) # equivalent to read_all_blocks()


        seg_nwb = r.read_block()        
        self.assertTrue(seg, Segment)
        self.assertTrue(seg_nwb, Segment)
        self.assertTrue(seg_nwb, seg)
        self.assertIsNotNone(seg_nwb, seg)

    def test_analogsignals_neo(self, **kargs):
        sig_neo = AnalogSignal(signal=[1, 2, 3], units='V', t_start=np.array(3.0)*pq.s, sampling_rate=1*pq.Hz)
        self.assertTrue(isinstance(sig_neo, AnalogSignal))
        r = NWBIO(filename=self.files_to_download[0], mode='r')
#        obj_nwb = r.read()
        obj_nwb = r.read_block()        
        self.assertTrue(obj_nwb, AnalogSignal)
        self.assertTrue(obj_nwb, sig_neo)

    
    def test_read_irregularlysampledsignal(self, **kargs):
        irsig0 = IrregularlySampledSignal([0.0, 1.23, 6.78], [1, 2, 3], units='mV', time_units='ms')
        irsig1 = IrregularlySampledSignal([0.01, 0.03, 0.12]*pq.s, [[4, 5], [5, 4], [6, 3]]*pq.nA)
        self.assertTrue(isinstance(irsig0, IrregularlySampledSignal))
        self.assertTrue(isinstance(irsig1, IrregularlySampledSignal))
        r = NWBIO(filename=self.files_to_download[0], mode='r')
#        irsig_nwb = r.read()
        irsig_nwb = r.read_block()        
        self.assertTrue(irsig_nwb, IrregularlySampledSignal)
        self.assertTrue(irsig_nwb, irsig0)
        self.assertTrue(irsig_nwb, irsig1)

    def test_read_event(self, **kargs):
        evt_neo = Event(np.arange(0, 30, 10)*pq.s, labels=np.array(['trig0', 'trig1', 'trig2'], dtype='S'))
        r = NWBIO(filename=self.files_to_download[0], mode='r')
#        event_nwb = r.read()
        event_nwb = r.read_block()
        self.assertTrue(event_nwb, evt_neo)
        self.assertIsNotNone(event_nwb, evt_neo)

    def test_read_epoch(self, **kargs):
        epc_neo = Epoch(times=np.arange(0, 30, 10)*pq.s,
                    durations=[10, 5, 7]*pq.ms,
                    labels=np.array(['btn0', 'btn1', 'btn2'], dtype='S'))
        r = NWBIO(filename=self.files_to_download[0], mode='r')
#        epoch_nwb = r.read()
        epoch_nwb = r.read_block()
        self.assertTrue(epoch_nwb, Epoch)
        self.assertTrue(epoch_nwb, epc_neo)
        self.assertIsNotNone(epoch_nwb, epc_neo)



    def test_write_NWB_File(self):
        '''
        Test function to write a segment.
        '''
        # Create a Block with 1 Segment and 2 ChannelIndex objects
        blocks = []
        num_segment=1 # number of segment
        segment_durations = [5*pq.s, 13*pq.s]

        for ind in range(2): # loop on blocks
            blk = Block(name='block_%s' %ind)            

            for seg_num in range(num_segment): # loop on segments
                seg = Segment(name=f'Seg {seg_num}')                
                blk.segments.append(seg)

                for seg_index in range(num_segment): # loop on ChannelIndex
                    sampling_rate = 80*pq.Hz
                    num_channel = 2
                    duration = segment_durations[seg_index]
                    length = int((sampling_rate*duration).simplified)
                    np_sig = np.random.randn(length, num_channel).astype('float32')

                    anasig = AnalogSignal(np_sig, units='cm', sampling_rate=sampling_rate)                    
                    anasig.annotate(data_type='tracking')
                    anasig.array_annotate(channel_names=['lfp_{}'.format(ch) for ch in range(num_channel)])
                    blk.segments[seg_index].analogsignals.append(anasig) #   
            blocks.append(blk)




#        for num_blk in range(2): # for 2 blocks
#            blk = Block(name='%s' %num_blk)
#            for ind in range(2): 
#                seg = Segment(name='segment_%d' % ind, index=ind)
#                blk.segments.append(seg)
##                blocks.append(blk)
#
#        blk = Block()
#        for ind in range(1):
#            seg = Segment(name='segment_%d' % ind, index=ind)
#            blk.segments.append(seg)
#
#            for ind in range(2):       
#                chx = ChannelIndex(name='Array probe %d' % ind, index=np.arange(64))
#                blk.channel_indexes.append(chx)
#
#            # Populate the Block with AnalogSignal objects
#            for seg in blk.segments:
#                for chx in blk.channel_indexes:
#                    # AnalogSignal
#                    a = AnalogSignal(signal=[1, 2, 3], units='V', t_start=np.array(3.0)*pq.s, sampling_rate=1*pq.Hz)
#                    chx.analogsignals.append(a)
#                    seg.analogsignals.append(a)
#                    # SpikeTrain
#                    t = SpikeTrain([3, 4, 5]*pq.s, t_stop=10.0)
#                    seg.spiketrains.append(t)
#                    # Epoch
#                    epc = Epoch(times=np.arange(0, 30, 10)*pq.s, 
#                                durations=[10, 5, 7]*pq.ms
#                                )
#                    seg.epochs.append(epc)
#                    # Event
#                    evt = Event(np.arange(0, 30, 20)*pq.s)
#                    seg.events.append(evt)
#                    # Unit
#                    unit = Unit(name='pyramidal neuron')
#                    unit.spiketrains.append(t)
#                	# IrregularlySampledSignal
#                    seg.irregularlysampledsignals.append(a)
#        print("blocks = ", blocks)

        # Save the file
        filename = '/home/elodie/env_NWB_py3/my_notebook/my_first_test_neo_to_nwb_test_NWBIO.nwb'
        w_file = NWBIO(filename=filename, mode='w') # Write the .nwb file
        print("w_file = ", w_file)
        blocks = w_file.write(blk)
#        blocks = w_file.write_all_blocks(blk)

        




    """
    def test_2_write_NWB_File(self):
        blocks = []
        for ind in range(2): # 2 blocks
            blk = Block(name='%s' %ind)
            blocks.append(blk)
    
            for ind in range(3): # 3 Segment
                seg = Segment(name='segment %d' % ind, index=ind)
                blk.segments.append(seg)
    
            for ind in range(2):  # 2 ChannelIndex
                chx = ChannelIndex(name='Array probe %d' % ind, index=np.arange(64))
                blk.channel_indexes.append(chx)
    
            for seg in blk.segments: # AnalogSignal objects
                for chx in blk.channel_indexes:
                    a = AnalogSignal(np.random.randn(10000, 64)*pq.nA, sampling_rate=10*pq.kHz)
                    chx.analogsignals.append(a)
                    seg.analogsignals.append(a)


         # Save the file
        filename = '/home/elodie/env_NWB_py3/my_notebook/second_first_test_neo_to_nwb_test_NWBIO.nwb'
        w_file = NWBIO(filename=filename, mode='w') # Write the .nwb file
        print("w_file = ", w_file)
        blocks = w_file.write(blk)
#        blocks = w_file.write_all_blocks(blk)
    """












    """
    def test_write_all_NWB_Files(self):
        '''
        Test function to write all blocks.
        '''
        # Create a Block with 1 Segment and 2 ChannelIndex objects
        blocks = []
        num_segment=1 # number of segment
        segment_durations = [5*pq.s, 13*pq.s]

        for ind in range(2): # loop on blocks
            blk = Block(name='block_%s' %ind)            

            for seg_num in range(num_segment): # loop on segments
                seg = Segment(name=f'Seg {seg_num}')                
                blk.segments.append(seg)

                for seg_index in range(num_segment): # loop on ChannelIndex
                    sampling_rate = 80*pq.Hz
                    num_channel = 2
                    duration = segment_durations[seg_index]
                    length = int((sampling_rate*duration).simplified)
                    np_sig = np.random.randn(length, num_channel).astype('float32')

                    anasig = AnalogSignal(np_sig, units='cm', sampling_rate=sampling_rate)                    
                    anasig.annotate(data_type='tracking')
                    anasig.array_annotate(channel_names=['lfp_{}'.format(ch) for ch in range(num_channel)])
                    blk.segments[seg_index].analogsignals.append(anasig) #   
            blocks.append(blk)

        # Save the file
        filename = '/home/elodie/env_NWB_py3/my_notebook/my_first_test_neo_to_nwb_test_NWBIO_all_blocks.nwb'
        w_file = NWBIO(filename=filename, mode='w') # Write the .nwb file
        print("w_file = ", w_file)
        blocks = w_file.write_all_blocks(blk)
    """


if __name__ == "__main__":
    print("pynwb.__version__ = ", pynwb.__version__)
    unittest.main()