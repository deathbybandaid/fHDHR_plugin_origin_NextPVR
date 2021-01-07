import xmltodict
import json


class OriginChannels():

    def __init__(self, fhdhr, origin):
        self.fhdhr = fhdhr
        self.origin = origin

    def get_channel_thumbnail(self, channel_id):
        channel_thumb_url = ("%s%s:%s/service?method=channel.icon&channel_id=%s" %
                             ("https://" if self.fhdhr.config.dict["origin"]["ssl"] else "http://",
                              self.fhdhr.config.dict["origin"]["address"],
                              str(self.fhdhr.config.dict["origin"]["port"]),
                              str(channel_id)
                              ))
        return channel_thumb_url

    def get_channels(self):

        data_url = ('%s%s:%s/service?method=channel.list&sid=%s' %
                    ("https://" if self.fhdhr.config.dict["origin"]["ssl"] else "http://",
                     self.fhdhr.config.dict["origin"]["address"],
                     str(self.fhdhr.config.dict["origin"]["port"]),
                     self.origin.sid
                     ))

        data_req = self.fhdhr.web.session.get(data_url)
        data_dict = xmltodict.parse(data_req.content)

        if 'channels' not in list(data_dict['rsp'].keys()):
            self.fhdhr.logger.error("Could not retrieve channel list")
            return []

        channel_o_list = data_dict['rsp']['channels']['channel']

        channel_list = []
        for c in channel_o_list:
            dString = json.dumps(c)
            channel_dict = eval(dString)

            clean_station_item = {
                                 "name": channel_dict["name"],
                                 "callsign": channel_dict["name"],
                                 "number": channel_dict["formatted-number"],
                                 "id": channel_dict["id"],
                                 "thumbnail": self.get_channel_thumbnail(channel_dict["id"])
                                 }
            channel_list.append(clean_station_item)
        return channel_list

    def get_channel_stream(self, chandict, stream_args):
        streamurl = ('%s%s:%s/live?channel_id=%s&client=%s' %
                     ("https://" if self.fhdhr.config.dict["origin"]["ssl"] else "http://",
                      self.fhdhr.config.dict["origin"]["address"],
                      str(self.fhdhr.config.dict["origin"]["port"]),
                      str(chandict["origin_id"]),
                      "fhdhr_" + str(chandict["origin_number"]),
                      ))

        stream_info = {"url": streamurl}

        return stream_info
