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

#to build the docker image, run the following command in the terminal

# docker pull manusharansah/insurance_premium_predictor:latest

#docker run -d \                                            
#-p 8000:8000 \
#-p 8501:8501 \
#--name new_insurance_app \
#manusharansah/insurance_premium_predictor:latest

#remove comment before running the above commands