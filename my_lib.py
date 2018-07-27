import re
import math 
import numpy as np

class IP:
    
    def __init__(self, ip_address):
        """
        This is used to print the information about the IP address
        """
        self.sep_ip = ip_address.strip().split('.')
        self.bin_ip = [bin(int(i))[2:].zfill(8) for i in self.sep_ip]
        self.bin_ip = "".join(self.bin_ip)
        self.classless_mask = None
        
    def info(self):
        """Describes the information about IP address"""
        show_block_info = True
        if self.bin_ip[0] == '0':
            _class = 'A'
            mask = 8
        else:
            if self.bin_ip[:2] == '10':
                _class = 'B'
                mask = 16
            elif self.bin_ip[:3] == '110':
                _class = 'C'
                mask = 24
            elif self.bin_ip[:4] == '1110':
                _class = 'D'
                show_block_info == False
            elif self.bin_ip[:4] == '1111':
                _class = 'E'
                show_block_info == False
            else:
                _class = '?'
                show_block_info = False
        
        if show_block_info:
            _range, _first_ip, _last_ip = self._apply_mask(mask)
            _first_ad =  self.dotted_decimal(_first_ip)
            _last_ad = self.dotted_decimal(_last_ip)
            
        show_cless_info = False if self.classless_mask is None else True
        if show_cless_info:
            _cless_range, _cless_first_ad, _cless_last_ad = self._apply_mask(self.classless_mask)
            _cless_first_ad = self.dotted_decimal(ip=_cless_first_ad, no_cache=True)
            _cless_last_ad = self.dotted_decimal(ip=_cless_last_ad, no_cache=True)

        print()		
        print('%-20s: %s' % ('Dotted-Decimal', self.dotted_decimal()))
        print('%-20s: %s' % ('Binary', self.bin_ip))
        print()
        if show_block_info:
            print('Classful Addressing Scheme:')
            print('%-20s: %s' % ('Class', _class))
            print('%-20s: %s' % ('Network mask', mask))
            print('%-20s: %s' % ('Range', _range))
            print('%-20s: %s' % ('Network address', _first_ad))
            print('%-20s: %s' % ('Broadcast address', _last_ad))

        if show_cless_info:
            print()
            print('Classless Addressing Scheme:'.format(_class))
            print('%-20s: %s' % ('Network mask', self.classless_mask))
            print('%-20s: %s' % ('Range', _cless_range))
            print('%-20s: %s' % ('Network address', _cless_first_ad))
            print('%-20s: %s' % ('Broadcast address', _cless_last_ad))


        print()        
        return
    
    
    def _apply_mask(self, mask, ip=None):
        """
        Applies mask on the current ip with value n=mask and returns 3 things.
        range of the IP block, first address, last address
        """ 
        _range = 2 ** (32 - mask)
        _network_mask = '1' * mask + '0' * (32 - mask)
        if ip == None:
            _ip = self.bin_ip
        else:
            _ip = ip

        _first_address = self._bitwise_and(_ip, _network_mask)
        _last_address = self._bitwise_or(_ip, self._bitwise_not(_network_mask))

        return _range, _first_address, _last_address

    #####################
    # Utility Functions #
    #####################
    
    def _bin_to_dec(self, value):
        temp = ''
        for i in range(0, 32, 8):
            temp += str(int(value[i:i+8], 2)) + '.'

        return temp
    
    def dotted_decimal(self, ip=None, no_cache=False):
        '''
        Returns the dotted decimal form of the address.
		'''
			# Convert 32-bit binary to dotted-decimal
        if ip == None:
            bin_ip = self.bin_ip
        else:
            bin_ip = ip
        dec_vals = []
        for i in range(0, 32, 8):
            bin_val = bin_ip[i:i+8]
            dec_val = int(bin_val, 2)
            dec_vals.append(dec_val)

        dec_ip = '.'.join([ str(dec) for dec in dec_vals])
        
        return dec_ip
    
    def _bitwise_and(self, ip1, ip2):
        '''
        Takes bitwise AND operation on two IPs
        '''
        _bin_ip1 = ip1
        _bin_ip2 = ip2
        _bin_and = ['1' if x==y=='1' else '0' for x, y in zip(_bin_ip1, _bin_ip2)]

        return ''.join([ _ for _ in _bin_and])

    def _bitwise_not(self, ip1):
        '''
        Takes bitwise NOT operation on IP
        '''
        _bin_ip = ip1
        return _bin_ip.translate(str.maketrans('01', '10'))

    def _bitwise_or(self, ip1, ip2):
        '''
        Takes bitwise OR operation on IP
        '''
        _bin_ip1 = ip1
        _bin_ip2 = ip2
        _bin_or = ['1' if x=='1' or y=='1' else '0' for x, y in zip(_bin_ip1, _bin_ip2)]

        return ''.join([ _ for _ in _bin_or])

    
my_ip = IP('150.68.0.0')
my_ip.info()
