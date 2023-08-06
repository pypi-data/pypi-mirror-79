from gurutools.bindings.pusher import activity_update
from gurutools.bindings.pusher import delegate_push

class ActionFormMixin:

    def post_process(self, channel, request, context_object, serializer, custom_message):
        """
        stream_message = self.get_stream_message(request, view, appointment)
        self.post_process(
            appointment.practitioner.channel,
            request,
            appointment,
            AppointmentListSerializer,
            stream_message
        )
        """
        # push to cache
        # todo
        if getattr(self, 'action_id', None) is None:
            raise Exception('Please define `action_id` on you Form. action_id should match the action_id from the action registry')

        context = serializer(context_object).data
        actor_id = request.user.id

        # push to stream:
        activity_update(
            actor_id,
            'appointmentview', # feed
            self.action_id,
            context,
            custom_message
        )

        # push to pubnub:
        delegate_push(
            method_name = "push_to_pubnub",
            args = (channel, context),
            version = "1"
        )