from django.views.generic.base import TemplateView
from domain.models import Message


class IndexView(TemplateView):
    template_name = "domain/index.html"

    def get_context_data(self, **kwargs):
        messages = Message.objects.all()[:10]

        context = super().get_context_data(**kwargs)
        context.update({'messages': messages})

        return context

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request, *args, **kwargs):
        message = request.POST.get('message')
        found, start, end, probable = self.parse_text(message, 'gmailcom')

        params = {
            'origin_message': message,
            'message_element': '',
            'resolution': 'does not contain',
            'found': int(found),
            'probable': int(probable)
        }

        if found:
            if probable:
                params['resolution'] = 'can contain'
            else:
                params['resolution'] = 'contains'

            params['message_element'] = message[start:end]

        if message:
            Message.objects.create(
                origin_message=message,
                message_element=params['message_element'] or '---',
                probable=probable,
                found=found,
                resolution=params['resolution'],
                ip=self.get_client_ip(request)
            )

        context = self.get_context_data(**kwargs)
        context.update(params)
        return self.render_to_response(context)

    def parse_text(self, text: str, domain: str, is_uncertain=False):
        sequence = [elem.lower() for elem in domain if elem.isalpha()]
        start_index = sequence_index = 0
        sequence_last_index = len(sequence) - 1
        in_sequence = False

        text = text.lower()
        text = text.replace('dot', '...').replace('at', '..').replace('0', 'o')

        for text_index, symbol in enumerate(text):
            if symbol.isalpha():
                if not in_sequence and symbol == sequence[sequence_index]:
                    in_sequence = True
                    start_index = text_index
                    continue

                if in_sequence and symbol == sequence[sequence_index]:
                    continue

                if in_sequence and symbol == sequence[sequence_index + 1]:
                    if sequence_index + 1 == sequence_last_index:
                        offset = 1
                        next_index = text_index + 1
                        try:
                            while text[next_index] == sequence[sequence_last_index]:
                                offset += 1
                                next_index += 1
                        except IndexError:
                            pass

                        try:
                            is_uncertain = text[next_index].isalpha()
                        except IndexError:
                            pass

                        return True, start_index, text_index + offset, is_uncertain

                    sequence_index += 1
                    continue

                if in_sequence:
                    in_sequence = False
                    start_index = 0
                    sequence_index = 0

        return False, 0, 0, is_uncertain