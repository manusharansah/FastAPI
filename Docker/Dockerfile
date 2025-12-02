#base image
FROM python:3.13.3

#working directory
WORKDIR /app

#copy files
COPY . /app


#requirements
RUN pip install -r requirements.txt
RUN chmod +x ./commands.sh
RUN chmod a+r *
RUN pip install scikit-learn



#environment
ENV PYTHONPATH=/app

#port
EXPOSE 8501
EXPOSE 8000

#command
CMD ["./commands.sh"]