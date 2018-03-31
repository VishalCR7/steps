(function () {
    var Message;
    Message = function (arg) {
        this.text = arg.text, this.message_side = arg.message_side;
        this.draw = function (_this) {
            return function () {
                var $message;
                $message = $($('.message_template').clone().html());
                $message.addClass(_this.message_side).find('.text').html(_this.text);
                $('.messages').append($message);
                return setTimeout(function () {
                    return $message.addClass('appeared');
                }, 0);
            };
        }(this);
        return this;
    };
    $(function () {
        var getMessageText, message_side, sendMessage;
        message_side = 'right';
        getMessageText = function () {
            var $message_input;
            $message_input = $('.message_input');
            return $message_input.val();
        };
        sendMessage = function (text) {
            var $messages, message;
            if (text.trim() === '') {
                return;
            }
            $('.message_input').val('');
            $messages = $('.messages');
            message_side = message_side === 'left' ? 'right' : 'left';
            message = new Message({
                text: text,
                message_side: message_side
            });
            message.draw();
            return $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
        };
        $('.send_message1').click(function (e) {
            var msg = getMessageText();
            sendMessage(msg);
            console.log(msg);
            $.post("/bot/",
            {
              'message': msg,
          },
          function(data, status){
            console.log(data.message);
            return sendMessage(data.message);
        });
            return 1
        });
        $('.message_input').keyup(function (e) {
            if (e.which === 13) {
                var msg = getMessageText();
                sendMessage(msg);
                console.log(msg);
                $.post("/bot/",
                {
                  'message': msg,
              },
              function(data, status){
                console.log(data.message);
                return sendMessage(data.message);
            });
                return 1
                return sendMessage(getMessageText());
            }
        });
        var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        var recognition = new SpeechRecognition();
        recognition.onresult = function(event) {
            var current = event.resultIndex;
            var transcript = event.results[current][0].transcript;
            sendMessage(transcript);
            $.post("/bot/",
            {
              'message': transcript,
          },
          function(data, status){
            console.log(data.message);
            return sendMessage(data.message);
        });
        }
        $('#start-record-btn').on('click', function(e) {
            recognition.start();
        });
        $('#pause-record-btn').on('click', function(e) {
            recognition.stop();
        });
});
}.call(this));
