
#the following code is taken from OsuDbReader licensed GPL. https://github.com/Awlexus/PyOsuDBReader/
#for some reason it's not a pypi package, so I had to just copypaste this in. I might PR to make it pypi compat though.
class BasicDbReader:
    def __init__(self, file):
        """
        Initializes a BasicDbReader on the given file.
        :param file: path to the db file
        """
        if not file or not os.path.exists(file):
            raise FileNotFoundError('Could not find from the specified file "%s"' % file)
        self.file = open(file, mode='rb')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def read_byte(self):
        """
        Read one Byte from the database-file
        """
        return int.from_bytes(self.file.read(1), byteorder='little')

    def read_short(self):
        """
        Read a Short (2 Byte) from the database-file
        """
        return int.from_bytes(self.file.read(2), byteorder='little')

    def read_int(self):
        """
        Read an Integer (4 Bytes) from the database-file
        """
        return int.from_bytes(self.file.read(4), byteorder='little')

    def read_long(self):
        """
        Read a Long (8 bytes) from the database-file
        """
        return int.from_bytes(self.file.read(8), byteorder='little')

    def read_uleb128(self):
        """
        Read a ULEB128 (variable) from the database-file
        """
        result = 0
        shift = 0
        while True:
            byte = int.from_bytes(self.file.read(1), byteorder='little')
            result |= ((byte & 127) << shift)
            if (byte & 128) == 0:
                break
            shift += 7
        return result

    def read_single(self):
        """
        Read a Single (4 bytes) from the database-file
        """
        return struct.unpack('f', self.file.read(4))[0]

    def read_double(self):
        """
        Read a Double (8 bytes) from the database-file
        """
        return struct.unpack('d', self.file.read(8))[0]

    def read_boolean(self):
        """
        Read a Boolean (1 byte) from the database-file
        """
        return self.read_byte() != 0

    def read_string(self):
        """
        Read a string (variable) from the database-file
        """
        if self.read_byte() == 0x0b:
            length = self.read_uleb128()
            return self.file.read(length).decode('utf8')

    def read_datetime(self):
        """
        Read a Datetime from the database-file
        """
        return self.read_long()
class OsuDbReader(BasicDbReader):
    def __init__(self, file=None):
        super(OsuDbReader, self).__init__(file)
        self.version = self.read_int()
        self.folder_count = self.read_int()
        self.unlocked = self.read_boolean()
        self.date_unlocked = self.read_datetime()
        self.player = self.read_string()
        self.num_beatmaps = self.read_int()
        self.beatmaps = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def read_int_double_pair(self):
        """
        Read an int-double-pair (14 bytes) from the database-file
        :return: a tuple with the int and the double
        """
        if self.read_byte() != 0x08:
            raise Exception('Error while parsing db.')

        first = self.read_int()
        if self.read_byte() != 0x0d:
            raise Exception('Error while parsing db.')
        second = self.read_double()
        return first, second

    def _read_timingpoint(self):
        """
        Read a Timingpoint (17 bytes) from the database-file
        :return: a dict containing bpm, offset and whether the timingpoint is inherited
        """
        bpm = self.read_double()
        offset = self.read_double()
        inherited = self.read_boolean()

        return {
            'bpm': bpm,
            'offset': offset,
            'inherited': inherited
        }

    def read_beatmap(self):
        """
        Read one Beatmap from the database-file
        :return: a (big) dict representing the beatmap
        """
        if len(self.beatmaps) >= self.num_beatmaps:
            return
        if(self.version<=20191106):
            entry_size = self.read_int()
        artist = self.read_string()
        artist_unicode = self.read_string()
        title = self.read_string()
        title_unicode = self.read_string()
        creator = self.read_string()
        difficulty = self.read_string()
        audio_file = self.read_string()
        md5 = self.read_string()
        osu_file = self.read_string()
        ranked_status = self.read_byte()
        circle_count = self.read_short()
        slider_count = self.read_short()
        spinner_count = self.read_short()
        last_modification_time = self.read_long()
        ar = self.read_single()
        cs = self.read_single()
        hp = self.read_single()
        od = self.read_single()
        slider_velocity = self.read_double()

        # Difficulties in respect with the selected mod
        difficulties_std = {}
        difficulties_taiko = {}
        difficulties_ctb = {}
        difficulties_mania = {}

        length = self.read_int()
        for _ in range(length):
            mode, diff = self.read_int_double_pair()
            difficulties_std[mode] = diff

        length = self.read_int()
        for _ in range(length):
            mode, diff = self.read_int_double_pair()
            difficulties_taiko[mode] = diff

        length = self.read_int()
        for _ in range(length):
            mode, diff = self.read_int_double_pair()
            difficulties_ctb[mode] = diff

        length = self.read_int()
        for _ in range(length):
            mode, diff = self.read_int_double_pair()
            difficulties_mania[mode] = diff

        drain_time = self.read_int()
        total_time = self.read_int()
        preview_time = self.read_int()

        # Timingpoints
        timing_points = []
        length = self.read_int()
        for _ in range(length):
            timing_points.append(self._read_timingpoint())

        map_id = self.read_int()
        set_id = self.read_int()
        thread_id = self.read_int()
        grade_std = self.read_byte()
        grade_taiko = self.read_byte()
        grade_ctb = self.read_byte()
        grade_mania = self.read_byte()
        local_offset = self.read_short()
        stack_leniency = self.read_single()
        game_mode = self.read_byte()  # 0x00 = osu!Standard, 0x01 = Taiko, 0x02 = CTB, 0x03 = Mania
        song_source = self.read_string()
        song_tags = self.read_string()
        online_offset = self.read_short()
        font = self.read_string()  # Why do you even need this -_-
        unplayed = self.read_boolean()
        last_played = self.read_long()
        osz2 = self.read_boolean()
        folder_name = self.read_string()
        last_checked = self.read_long()
        ignore_map_sound = self.read_boolean()
        ignore_map_skin = self.read_boolean()
        disable_storyboard = self.read_boolean()
        disable_video = self.read_boolean()
        visual_override = self.read_boolean()  # I have no idea what that is supposed to be
        last_modification_time_2 = self.read_int()  # I swear we had this already
        mania_scroll_speed = self.read_byte()

        beatmap = {'artist': artist, 'artist_unicode': artist_unicode, 'title': title,
                   'title_unicode': title_unicode, 'creator': creator, 'difficulty': difficulty,
                   'audio_file': audio_file, 'md5': md5, 'osu_file': osu_file, 'ranked_status': ranked_status,
                   'circle_count': circle_count, 'slider_count': slider_count, 'spinner_count': spinner_count,
                   'last_modification_time': last_modification_time, 'ar': ar, 'cs': cs, 'hp': hp, 'od': od,
                   'slider_velocity': slider_velocity, 'difficulties_std': difficulties_std,
                   'difficulties_taiko': difficulties_taiko, 'difficulties_ctb': difficulties_ctb,
                   'difficulties_mania': difficulties_mania, 'drain_time': drain_time, 'total_time': total_time,
                   'preview_time': preview_time, 'timing_points': timing_points, 'map_id': map_id, 'set_id': set_id,
                   'thread_id': thread_id, 'grade_std': grade_std, 'grade_taiko': grade_taiko, 'grade_ctb': grade_ctb,
                   'grade_mania': grade_mania, 'local_offset': local_offset, 'stack_leniency': stack_leniency,
                   'game_mode': game_mode, 'song_source': song_source, 'song_tags': song_tags,
                   'online_offset': online_offset, 'font': font, 'unplayed': unplayed, 'last_played': last_played,
                   'osz2': osz2, 'folder_name': folder_name, 'last_checkee': last_checked,
                   'ignore_map_sound': ignore_map_sound, 'ignore_map_skin': ignore_map_skin,
                   'disable_storyboard': disable_storyboard, 'disable_video': disable_video,
                   'visual_override': visual_override, 'last_modification_time_2': last_modification_time_2,
                   'mania_scroll_speed': mania_scroll_speed}
        self.beatmaps.append(beatmap)
        return beatmap

    def read_all_beatmaps(self):
        for i in range(self.num_beatmaps - len(self.beatmaps)):
            self.read_beatmap()
        return self.beatmaps
